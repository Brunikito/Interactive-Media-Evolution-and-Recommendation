from src.recommendation.recommendate import recommendate
import pandas as pd
import numpy as np
import time

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
def create_random_uwatching_cont(
    num_watching_ratio,
    users,
    USERS,
    content,
    CONTENT,
    uwatchingcont,
    content_tags,
    userinteraction,
    ucontint,
    comment,
    livecomment,
    videocomment,
    shortcomment,
    num_recommendations,
    current_datetime
):
    rng = np.random.default_rng()

    total_start = time.time()  # Timer total da função

    # 1. Filtrar usuários que estão assistindo no máximo 4 conteúdos
    start = time.time()
    watching_now = uwatchingcont[uwatchingcont['UIsWatchingCONTNow']]
    if watching_now.empty:
        valid_users = users.copy()
    else:
        counts = watching_now.groupby("UserID").size()
        valid_user_ids = counts[counts <= 4].index.values
        valid_users = users[users['user_id'].isin(valid_user_ids)].reset_index(drop=True)
    print(f"Etapa 1 - Filtragem de usuários: {time.time() - start:.4f}s")

    # 2. Amostragem de usuários
    start = time.time()
    num_users = int(valid_users.shape[0] * num_watching_ratio)
    user_sampled = valid_users.sample(num_users, replace=False).reset_index(drop=True)
    user_ids = user_sampled['user_id'].values.astype(np.int32)
    USER_sampled = USERS.iloc[user_ids]
    print(f"Etapa 2 - Amostragem de usuários: {time.time() - start:.4f}s")

    # 3. Geração de recomendações
    start = time.time()
    print('Antes de recomendar')
    recommendations = recommendate(
        num_recommendations, 
        USER_sampled, 
        CONTENT, 
        uwatchingcont, 
        content_tags, 
        userinteraction,
        ucontint,
        comment,
        livecomment,
        videocomment,
        shortcomment)
    print(recommendations[-10:])
    rec_matrix = recommendations[:, 1].reshape((num_users, num_recommendations))
    print('Depois de recomendar')
    print(f"Etapa 3 - Recomendações: {time.time() - start:.4f}s")

    # 4. Escolha entre recomendação ou conteúdo aleatório
    start = time.time()
    use_recommendation = rng.random(num_users) < 0.6
    random_indices = rng.integers(0, num_recommendations, size=num_users)
    recommended_contents = rec_matrix[np.arange(num_users), random_indices]
    random_contents = rng.choice(content["content_id"].values, size=num_users)
    final_contents = np.where(use_recommendation, recommended_contents, random_contents).astype(np.int32)
    print(f"Etapa 4 - Seleção de conteúdo: {time.time() - start:.4f}s")

    # 5. Determinação de durações assistidas
    start = time.time()
    content_ids_arr = content["content_id"].values
    durations_arr = content["content_duration"].values
    content_duration_map = dict(zip(content_ids_arr, durations_arr))
    durations = np.array([content_duration_map[cid] for cid in final_contents], dtype=np.float32)
    watched_durations = rng.beta(2, 2, size=num_users) * durations
    print(f"Etapa 5 - Duração assistida: {time.time() - start:.4f}s")

    # 6. Criação dos IDs e do DataFrame final
    start = time.time()
    uwatch_ids = np.arange(uwatchingcont.shape[0], uwatchingcont.shape[0] + num_users, dtype=np.int32)
    df_new_watch = pd.DataFrame({
        'UWatchDurationCONT': watched_durations.astype(np.int16),
        'UWatchCONTDateTime': np.full(num_users, current_datetime),
        'UIsWatchingCONTNow': np.ones(num_users, dtype=bool),
        'UWATCHCONTID': uwatch_ids,
        'UserID': user_ids,
        'ContentID': final_contents
    })
    print(f"Etapa 6 - Criação do DataFrame: {time.time() - start:.4f}s")

    print(f"Tempo total da função: {time.time() - total_start:.4f}s")
    return df_new_watch


if __name__ == '__main__':
    from src import BASE_PATH, DATA_PATH
    import os
    num_watching_ratio = 1
    users = pd.read_parquet(os.path.join(BASE_PATH, 'usuarios_full.parquet'))
    USERS = pd.read_parquet(os.path.join(BASE_PATH, 'USERS.parquet'))
    content = pd.read_parquet(os.path.join(BASE_PATH, 'df_content.parquet'))
    CONTENT = pd.read_parquet(os.path.join(BASE_PATH, 'df_content_table.parquet'))
    uwatchingcont = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'UWATCHINGCONT.csv'))
    content_tags = pd.read_parquet(os.path.join(BASE_PATH, 'CONTENT_TAG.parquet'))
    userinteraction = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'USERINTERACTION.csv'))
    ucontint = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'UCONTINT.csv'))
    comment = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'COMMENT.csv'))
    livecomment = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'LIVECOMMENT.csv'))
    videocomment = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'VIDEOCOMMENT.csv'))
    shortcomment = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'SHORTCOMMENT.csv'))
    num_recommendations = 50
    current_datetime = 0
    print("Colunas do uwatchingcont:", uwatchingcont.columns)
    
    df_new_watch = create_random_uwatching_cont(
    num_watching_ratio,
    users,
    USERS,
    content,
    CONTENT,
    uwatchingcont,
    content_tags,
    userinteraction,
    ucontint,
    comment,
    livecomment,
    videocomment,
    shortcomment,
    num_recommendations,
    current_datetime
    )
    print(df_new_watch.head())
    
    df_new_watch.to_parquet(os.path.join(BASE_PATH, 'UWATCHINGCONT.parquet'))
    num_watching_ratio = 0.3
    before_time = time.time()
    for i in range(5):
        uwatchingcont = pd.read_parquet(os.path.join(BASE_PATH, 'UWATCHINGCONT.parquet'))
        df_new_watch = create_random_uwatching_cont(
        num_watching_ratio,
        users,
        USERS,
        content,
        CONTENT,
        uwatchingcont,
        content_tags,
        userinteraction,
        ucontint,
        comment,
        livecomment,
        videocomment,
        shortcomment,
        num_recommendations,
        current_datetime
        )
        uwatchingcont_updated = pd.concat([uwatchingcont, df_new_watch], ignore_index=True)
        uwatchingcont_updated.to_parquet(os.path.join(BASE_PATH, 'UWATCHINGCONT.parquet'), index=False)
    print(f'5 iterations: {time.time() - before_time}s')
    uwatchingcont = pd.read_parquet(os.path.join(BASE_PATH, 'UWATCHINGCONT.parquet'))
    df_new_watch = create_random_uwatching_cont(
        num_watching_ratio,
        users,
        USERS,
        content,
        CONTENT,
        uwatchingcont,
        content_tags,
        userinteraction,
        ucontint,
        comment,
        livecomment,
        videocomment,
        shortcomment,
        num_recommendations,
        current_datetime
        )
    print(df_new_watch.head())
    
    
        
    
    