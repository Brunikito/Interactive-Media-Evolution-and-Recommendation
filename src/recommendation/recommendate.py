import pandas as pd
import numpy as np
import time
import numba
# Cria array de listas (Numba List)
from numba.typed import Dict, List
from numba import types
from heapq import nlargest

'''recommendations = recommendate(
    n, 
    user_sampled, 
    content, 
    uwatchingcont, 
    content_tags, 
    userinteraction,
    ucontint,
    comment,
    livecomment,
    videocomment,
    shortcomment)
Vai retornar um ndarray com os ids dos usuarios na primeira coluna e as recomendacoes de conteudo para cada um deles.
O ndarray tem os seguintes campos:
    
        - [0]: o id do usuario
        - [1]: o id do conteudo recomendado para o usuario
        - [2]: o rank da recomendacao (1 a n)
'''

def get_map(content_id_arr, tags_arr):
    sort_idx = np.argsort(content_id_arr)
    content_ids_sorted = content_id_arr[sort_idx]
    tags_sorted = tags_arr[sort_idx]

    # 2. Encontrar onde os content_ids mudam
    # Isso marca o índice de início de cada novo content_id
    change_idx = np.where(np.diff(content_ids_sorted) != 0)[0] + 1
    split_indices = np.r_[0, change_idx, len(content_ids_sorted)]

    # 3. Slicing baseado nos índices detectados
    unique_content_ids = content_ids_sorted[split_indices[:-1]]  # pega um de cada grupo
    tag_slices = [tags_sorted[start:end] for start, end in zip(split_indices[:-1], split_indices[1:])]

    # 4. Se quiser converter em dict (rápido, sem append):
    content_tag_map = dict(zip(unique_content_ids, tag_slices))
    return content_tag_map

def recommendate(n, users, content, uwatchingcont, content_tags,
                 userinteraction, ucontint, comment,
                 livecomment, videocomment, shortcomment):

    total_start = time.time()
    print("📥 Preparando dados...")
    prep_start = time.time()

    ## Etapa 1: extração de colunas principais
    start = time.time()
    user_ids = users["UserID"].values.astype(np.int32)
    content_ids = content["ContentID"].values.astype(np.int32)
    content_categories = content["CONTCategory"].values.astype(np.int8)
    content_id_arr = content_tags["ContentID"].values.astype(np.int32)
    tags_arr = content_tags["CONTTag"].values.astype(np.int8)
    rng = np.random.default_rng()
    print(f"🧾 Extração de colunas principais: {time.time() - start:.4f}s")

    ## Etapa 2: processamento de tags
    start = time.time()
    content_tag_map = get_map(content_id_arr, tags_arr)
    print(f"🏷️ Mapeamento de tags por conteúdo (Improved): {time.time() - start:.4f}s")

    ## Etapa 3: categorias → conteúdos
    start = time.time()
    cat_to_content = {}
    for cid, cat in zip(content_ids, content_categories):
        cat_to_content.setdefault(cat, []).append(cid)
    print(f"🗂️ Mapeamento de categoria → conteúdos: {time.time() - start:.4f}s")
    
    ## Etapa 4: conteúdo → categoria
    start = time.time()
    content_id_to_category = dict(zip(content_ids, content_categories))
    print(f"📚 Mapeamento de conteúdo → categoria: {time.time() - start:.4f}s")

    ## Etapa 5: conteúdos assistidos
    start = time.time()
    watched_mask = uwatchingcont["UWatchDurationCONT"].values > 0
    uw_user_ids = uwatchingcont["UserID"].values[watched_mask].astype(np.int32)
    uw_content_ids = uwatchingcont["ContentID"].values[watched_mask].astype(np.int32)

    user_watched_map = {}
    for uid, cid in zip(uw_user_ids, uw_content_ids):
        user_watched_map.setdefault(uid, []).append(cid)
    print(f"🎬 Mapeamento de conteúdos assistidos: {time.time() - start:.4f}s")

    ## Etapa 6: curtidas e merge
    start = time.time()
    likes = userinteraction[userinteraction["UINTType"] == 1][["UserID", "UINTID"]]
    likes_with_content = likes.merge(ucontint, on="UINTID", how="inner")

    like_map = {}
    for uid, cid in zip(likes_with_content["UserID"], likes_with_content["ContentID"]):
        like_map.setdefault(uid, []).append(cid)
    print(f"❤️ Mapeamento de curtidas (com merge): {time.time() - start:.4f}s")

    ## Total da preparação
    print(f"✅ Dados mapeados em {time.time() - prep_start:.4f}s. Iniciando recomendação...\n")

    num_users = len(user_ids)
    # Garantir que temos elementos suficientes
    if len(content_ids) < n:
        raise ValueError("Não há conteúdos suficientes para realizar fallback com replace=False.")

    # Pré-gerar fallbacks únicos por usuário fora do loop
    # Amostra única de shape (num_users, n), sem repetição por usuário
    fallback_sample_init = time.time()
    fallback_global = rng.choice(content_ids, size=n, replace=False)
    # Cria base com fallback para todos
    user_ids_repeated = np.repeat(user_ids, n)
    ranks = np.tile(np.arange(1, n + 1), num_users)
    fallback_contents = np.tile(fallback_global, num_users)

    # Shape (num_users * n, 3)
    result_matrix = np.column_stack((user_ids_repeated, fallback_contents, ranks))
    user_row_start = [idx * n for idx, _ in enumerate(user_ids)]
    print(f'Finished fallback sample in: {time.time() - fallback_sample_init}s')

    # Timers acumulativos
    tag_time = 0.0
    cat_time = 0.0
    score_time = 0.0
    fallback_time = 0.0
    sort_time = 0.0
    likes_time = 0.0
    watch_time = 0.0
    loop_start = time.time()

    empty_array = np.zeros(16, dtype=np.int16)
    seen_tags = empty_array.copy()

    for user_idx, user_id in enumerate(user_ids):
        likes_start = time.time()
        liked = like_map.get(user_id, [])

        if not hasattr(liked, '__len__') or len(liked) == 0:
            fb_start = time.time()
            fallback_time += time.time() - fb_start
            likes_time += time.time() - likes_start
            continue
        
        watch_start = time.time()
        watched = user_watched_map.get(user_id, [])
        seen_content = set(watched).union(liked)
        watch_time += time.time() - watch_start
        
        # Contar tags
        tag_start = time.time()
        seen_tags[:] = 0
        for cid in watched:
            for tag in content_tag_map.get(cid, []):
                seen_tags[tag] += 1
        for cid in liked:
            for tag in content_tag_map.get(cid, []):
                seen_tags[tag] += 2
        tag_time += time.time() - tag_start

        # Categoria dominante
        cat_start = time.time()
        liked_cats = [content_id_to_category.get(cid) for cid in liked]
        main_cat = liked_cats[np.argmax(np.bincount(liked_cats))]
        candidate_cids = set(cat_to_content.get(main_cat, [])) - seen_content
        cat_time += time.time() - cat_start

        # Scoring
        score_start = time.time()
        scored = []
        for cid in candidate_cids:
            tags = content_tag_map.get(cid, [])
            score = np.sum(seen_tags[tags])
            if score > 0:
                scored.append((cid, score))
        score_time += time.time() - score_start

        if not scored:
            continue
        else:
            sort_start = time.time()
            top_scored_ids = [cid for cid, _ in nlargest(n, scored, key=lambda x: x[1])]
            start_idx = user_row_start[user_idx]
            length = len(top_scored_ids)
            result_matrix[start_idx:start_idx + length, 1] = top_scored_ids
            sort_time += time.time() - sort_start

    total_time = time.time() - total_start
    loop_total_time = time.time() - loop_start

    print("\n⏱️ Resumo de tempos:")
    print(f"🔁 Loop total:         {loop_total_time:.4f}s")
    print(f"   🏷️  Likes:           {likes_time:.4f}s")
    print(f"   🏷️  Visualizações:   {watch_time:.4f}s")
    print(f"   🏷️  Tags:            {tag_time:.4f}s")
    print(f"   🗂️  Categorias:      {cat_time:.4f}s")
    print(f"   📊 Scoring:         {score_time:.4f}s")
    print(f"   📉 Ordenação:       {sort_time:.4f}s")
    print(f"   🪂 Fallbacks:       {fallback_time:.4f}s")
    print(f"\n⏳ Tempo total função: {total_time:.4f}s\n")

    return np.array(result_matrix, dtype=np.int32)