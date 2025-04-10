import pandas as pd
import numpy as np
from collections import Counter

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
def recommendate(n, users, content, uwatchingcont, content_tags,
                 userinteraction, ucontint, comment,
                 livecomment, videocomment, shortcomment):

    print("📥 Preparando dados...")
    user_ids = users["UserID"].values.astype(np.int32)
    content_ids = content["ContentID"].values.astype(np.int32)
    content_categories = content["CONTCategory"].values
    rng = np.random.default_rng()

    # Mapeamento: ContentID → Tags
    content_id_arr = content_tags["ContentID"].values.astype(np.int32)
    tags_arr = content_tags["CONTTag"].values

    # ContentID → list(tags)
    content_tag_map = {}
    for cid, tag in zip(content_id_arr, tags_arr):
        content_tag_map.setdefault(cid, []).append(tag)

    # Categoria → ContentIDs
    cat_to_content = {}
    for cid, cat in zip(content_ids, content_categories):
        cat_to_content.setdefault(cat, []).append(cid)

    # ContentID → Categoria
    content_id_to_category = dict(zip(content_ids, content_categories))

    # Conteúdos assistidos
    watched_mask = uwatchingcont["UWatchDurationCONT"].values > 0
    uw_user_ids = uwatchingcont["UserID"].values[watched_mask].astype(np.int32)
    uw_content_ids = uwatchingcont["ContentID"].values[watched_mask].astype(np.int32)

    user_watched_map = {}
    for uid, cid in zip(uw_user_ids, uw_content_ids):
        user_watched_map.setdefault(uid, []).append(cid)

    # Likes → via UCONTINT
    likes = userinteraction[userinteraction["UINTType"] == 1][["UserID", "UINTID"]]
    likes_with_content = likes.merge(ucontint, on="UINTID", how="inner")
    like_map = {}
    for uid, cid in zip(likes_with_content["UserID"], likes_with_content["ContentID"]):
        like_map.setdefault(uid, []).append(cid)

    print("✅ Dados mapeados. Iniciando recomendação...")

    result_rows = []

    for user_id in user_ids:
        watched = user_watched_map.get(user_id, [])
        liked = like_map.get(user_id, [])
        seen_content = set(watched).union(liked)

        if not liked:
            # Sem curtidas → fallback direto
            fallback = rng.choice(content_ids, size=n, replace=False)
            result_rows.extend((user_id, cid, rank) for rank, cid in enumerate(fallback, 1))
            continue

        # Tags vistas com pesos (Counter aceita contagem)
        seen_tags = Counter()
        for cid in watched:
            for tag in content_tag_map.get(cid, []):
                seen_tags[tag] += 1
        for cid in liked:
            for tag in content_tag_map.get(cid, []):
                seen_tags[tag] += 2  # Peso 2 para likes

        # Categoria dominante com base nas curtidas
        liked_cats = [content_id_to_category.get(cid) for cid in liked]
        main_cat = Counter(liked_cats).most_common(1)[0][0]

        # Candidatos ainda não vistos, da categoria dominante
        candidate_cids = set(cat_to_content.get(main_cat, [])) - seen_content

        scored = []
        for cid in candidate_cids:
            tags = content_tag_map.get(cid, [])
            score = sum(seen_tags.get(tag, 0) for tag in tags)
            if score > 0:
                scored.append((cid, score))

        if not scored:
            fallback_pool = list(candidate_cids) if candidate_cids else content_ids
            fallback = rng.choice(fallback_pool, size=n, replace=False)
            result_rows.extend((user_id, cid, rank) for rank, cid in enumerate(fallback, 1))
        else:
            scored.sort(key=lambda x: -x[1])
            result_rows.extend((user_id, cid, rank) for rank, (cid, _) in enumerate(scored[:n], 1))

    return np.array(result_rows, dtype=np.int32)