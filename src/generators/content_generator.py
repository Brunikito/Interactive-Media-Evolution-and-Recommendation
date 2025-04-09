import pandas as pd
import numpy as np
import os
from src import DATA_PATH, BASE_PATH
from src.generators.feature_generators.cython.content_optimized import to_base62_fast, fast_hash, generate_languages_nogil, generate_tags_fast, generate_content_tags
# Pré-carregar dados
country_data = pd.read_csv(os.path.join(DATA_PATH, 'behavior_generated', 'country_data_cleaned.csv'))
languages = np.unique(np.concatenate(country_data['Languages'].str.split(',')))

CATEGORIES = np.array([
    'Animals', 'Automobiles', 'Science & Technology', 'Comedy', 'Education',
    'Entertainment', 'Sports', 'Film & Animation', 'How-to & Style', 'Gaming',
    'Music', 'News & Politics', 'People & Blogs', 'Nonprofits & Activism', 'Travel & Events'
    ], dtype=object)
    
# Inicializar categorias em cache

import time

def generate_languages_fast(channel_langs, use_channel_lang, languages, rng):
    # Gera todos aleatórios de uma vez
    random_langs = rng.choice(languages, size=len(channel_langs))

    # Extrai só o primeiro idioma de cada string (assumindo separado por vírgula)
    # Não faz loop: faz vetor de strings, aplica split, pega primeira parte
    first_langs = np.char.partition(channel_langs.astype(str), ',')[:, 0]

    # Combina de forma vetorial: onde usar canal, pega do canal, senão aleatório
    return np.where(use_channel_lang, first_langs, random_langs)

def create_random_content(channels, categories, content_ratio, initial_id, current_date):
    timings = {}
    t0 = time.perf_counter()
    num_content = int(len(channels) * content_ratio)
    rng = np.random.default_rng()

    # Seleção aleatória
    shuffled_idx = rng.choice(len(channels), size=num_content, replace=False)
    content_channel = channels.iloc[shuffled_idx]
    timings['select_channels'] = time.perf_counter() - t0

    # IDs e nomes
    t1 = time.perf_counter()
    content_id = np.arange(initial_id, initial_id + num_content, dtype=np.int32)
    channel_names = content_channel['channel_name'].values.astype(str)
    timings['ids_and_names'] = time.perf_counter() - t1

    # Títulos e data
    t1 = time.perf_counter()
    content_title = np.char.add(channel_names, ' Content ' + current_date)
    content_creation_date = np.full(num_content, current_date)
    timings['titles_and_data'] = time.perf_counter() - t1

    # Status
    t1 = time.perf_counter()
    content_status = rng.choice(['Public', 'Private', 'Unlisted'], size=num_content, p=[0.8, 0.1, 0.1])
    timings['status'] = time.perf_counter() - t1

    # Categorias
    t1 = time.perf_counter()
    channel_categories = content_channel['channel_category'].values
    use_channel_cat = rng.random(num_content) < 0.8
    content_category = np.where(use_channel_cat, channel_categories, rng.choice(categories, size=num_content))
    timings['category'] = time.perf_counter() - t1

    # Tags
    t1 = time.perf_counter()
    extra_tags = rng.choice(categories, size=num_content*2, replace=True)
    timings['tags_rng'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    content_tags_list = generate_tags_fast(content_category, extra_tags)
    timings['tags'] = time.perf_counter() - t1

    # Idiomas
    t1 = time.perf_counter()
    use_channel_lang = (rng.random(num_content) < 0.8).astype(np.uint8)
    channel_langs = np.array(content_channel['channel_language'].values, dtype='S')
    fallback_langs = np.array(rng.choice(languages, size=num_content), dtype='S')
    timings['languages_rng'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    content_language = generate_languages_nogil(use_channel_lang, channel_langs, fallback_langs)
    timings['languages'] = time.perf_counter() - t1

    # Métricas
    t1 = time.perf_counter()
    zeros = np.zeros(num_content, dtype=np.int32)
    content_view_count = content_like_count = content_dislike_count = content_comment_count = zeros
    timings['metrics'] = time.perf_counter() - t1

    # Tipo e duração
    t1 = time.perf_counter()
    content_type = rng.choice(['Video', 'Short', 'Live'], size=num_content, p=[0.6, 0.3, 0.1])
    content_duration = np.empty(num_content, dtype=np.float32)
    content_duration[content_type == 'Video'] = rng.beta(2, 4, (content_type == 'Video').sum()) * 60
    content_duration[content_type == 'Short'] = rng.beta(4, 2, (content_type == 'Short').sum()) * 60
    content_duration[content_type == 'Live'] = rng.beta(2, 3, (content_type == 'Live').sum()) * 18000
    timings['duration'] = time.perf_counter() - t1

    # Hashes
    t1 = time.perf_counter()
    encoded_ids = list(map(to_base62_fast, content_id))
    content_hashes = [fast_hash(f"{t}{e}") for t, e in zip(content_title, encoded_ids)]
    content_hashes_int = np.fromiter(
        (int(h, 16) for h in content_hashes),
        dtype=np.uint64,
        count=len(content_hashes)
    )
    timings['hashes'] = time.perf_counter() - t1

    # Rating
    t1 = time.perf_counter()
    content_rating = rng.choice(['General Audience', 'Kids', 'Default', 'Age-Restricted'], size=num_content, p=[0.35, 0.2, 0.35, 0.1])
    timings['rating'] = time.perf_counter() - t1
    
    t3 = time.perf_counter()
    t1 = time.perf_counter()
    # Tabela CONTENT
    df_content_table = pd.DataFrame({
        'ContentID': content_id.astype(np.int32),
        'ContentURL': content_hashes_int,
        'CONTTitle': content_hashes_int,
        'CONTPubDateTime': pd.Categorical(content_creation_date),
        'CONTStatus': pd.Categorical(content_status),
        'CONTCategory': pd.Categorical(content_category),
        'CONTLanguage': pd.Categorical(content_language),
        'CONTThumb': content_hashes_int,
        'CONTDesc': content_hashes_int,
        'CONTIndRating': pd.Categorical(content_rating),
        'ChannelID': content_channel['channel_id'].values.astype(np.int32),
    })
    timings['content_table'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()
    # Estatísticas
    df_CONTENT = pd.DataFrame(
        np.column_stack((content_id, content_view_count, content_like_count, content_dislike_count, content_comment_count)),
        columns=["ContentID", "Views", "Likes", "Dislikes", "Comments"]
    )

    timings['CONTENT'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()
    # Tags
    # Pré-processamento
    cid_subset = content_id.astype(np.int32)

    # Chamada Cython
    tag_rows = generate_content_tags(cid_subset, content_tags_list)

    # Conversão final
    df_content_tag = pd.DataFrame(tag_rows, columns=["CONTTag", "ContentID"])
    df_content_tag["CONTTag"] = pd.Categorical(df_content_tag["CONTTag"])
    df_content_tag["ContentID"] = df_content_tag["ContentID"].astype(np.int32)

    timings['content_tag'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()

    # Tipos de conteúdo
    df_video = df_content_table[content_type == "Video"][["ContentID"]].copy()
    video_hashes = np.array(content_hashes_int)[content_type == "Video"]
    df_video["VIDEOBody"] = video_hashes.astype(np.int64)

    timings['video'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()

    df_short = df_content_table[content_type == "Short"][["ContentID"]].copy()
    df_short["SHORTBody"] = "Default short body"
    short_hashes = np.array(content_hashes_int)[content_type == "Short"]
    df_short["SHMusicLink"] = short_hashes.astype(np.int64)

    timings['shorts'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()

    df_live = df_content_table[content_type == "Live"][["ContentID"]].copy()
    live_hashes = np.array(content_hashes_int)[content_type == "Live"]
    df_live["LIVEBody"] = live_hashes.astype(np.int64)

    timings['live'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()

    # Tabela content expandida
    df_content = pd.DataFrame({
        'content_id': content_id.astype(np.int32),
        'channel_id': content_channel['channel_id'].values.astype(np.int32),
        'content_title': content_hashes_int,
        'content_description': content_hashes_int,
        'content_status': pd.Categorical(content_status),
        'content_category': pd.Categorical(content_category),
        'content_language': pd.Categorical(content_language),
        'content_duration': content_duration.astype(np.float32),
        'content_creation_date': pd.Categorical(content_creation_date),
        'content_view_count': content_view_count.astype(np.int32),
        'content_like_count': content_like_count.astype(np.int32),
        'content_dislike_count': content_dislike_count.astype(np.int32),
        'content_comment_count': content_comment_count.astype(np.int32),
        'content_ind_rating': pd.Categorical(content_rating),
        'content_type': pd.Categorical(content_type),
        'content_is_live': (content_type == 'Live').astype(bool),
        'content_comments': np.zeros(num_content, dtype=bool),
    })

    timings['content'] = time.perf_counter() - t1
    
    timings['dataframes'] = time.perf_counter() - t3
    timings['total'] = time.perf_counter() - t0

    return {
        "df_content": df_content,
        "df_content_table": df_content_table,
        "df_CONTENT": df_CONTENT,
        "df_content_tag": df_content_tag,
        "df_video": df_video,
        "df_short": df_short,
        "df_live": df_live,
        "timings": timings
    }

if __name__ == '__main__':
    channels = pd.read_parquet(os.path.join(BASE_PATH, 'channels_full.parquet'))
    print('creating content...')
    start = time.perf_counter()
    result = create_random_content(channels, CATEGORIES, 1, 0, '2025-04-08')
    end = time.perf_counter()
    print('done')
    print('Time taken:', end - start)
    print("#"*50)

    def print_memory_usage(name, df):
        mem_mb = df.memory_usage(deep=True).sum() / 1024**2
        print(f"{name}: {mem_mb:.2f} MB")

    for name, df in result.items():
        if isinstance(df, pd.DataFrame):
            print_memory_usage(name, df)

    print("#"*50)
    mem_info = result['df_content'].memory_usage(deep=True).sort_values(ascending=False)
    print(mem_info / 1024**2)

    # Logs
    with open("timing_log.txt", "w") as f:
        f.write("Etapas de tempo para create_random_content:\n\n")
        for step, duration in result["timings"].items():
            f.write(f"{step}: {duration:.6f} segundos\n")
    
    