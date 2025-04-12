"""
Module: content_generator
-------------------------

Este módulo é responsável pela geração de conteúdo sintético (como vídeos, lives e shorts) com base nos canais existentes. 
Utiliza funções otimizadas em Cython para acelerar o processamento de linguagens, tags e hashes.

O conteúdo gerado inclui informações como título, categoria, status, idioma, duração, tipo e métricas, além de tabelas auxiliares 
para vídeos, shorts, lives e tags associadas. A geração é vetorizada e otimizada para escalabilidade.

Dependências:
- to_base62_fast, fast_hash: Funções otimizadas para codificação e hashing.
- generate_languages_nogil: Geração de idiomas com Cython sem GIL.
- generate_tags_fast: Geração vetorizada de tags por categoria.
- generate_content_tags: Mapeamento de conteúdo para tags.
"""

import pandas as pd
import numpy as np
import os
from src import DATA_PATH, BASE_PATH
from src.generators.feature_generators.cython.content_optimized import (
    to_base62_fast,
    fast_hash,
    generate_languages_nogil,
    generate_tags_fast,
    generate_content_tags
)
import time

# Pré-carrega dados de país e extrai lista única de idiomas
country_data = pd.read_parquet(os.path.join(DATA_PATH, 'behavior_generated', 'country_data_cleaned.parquet'))
languages = np.unique(np.concatenate(country_data['Languages'].str.split(',')))

# Categorias disponíveis
CATEGORIES = np.arange(1, 16, dtype=np.int8)

def generate_languages_fast(
    channel_langs: np.ndarray,
    use_channel_lang: np.ndarray,
    languages: np.ndarray,
    rng: np.random.Generator
) -> np.ndarray:
    """
    Gera vetorialmente os idiomas dos conteúdos com base na linguagem do canal ou um idioma aleatório.

    Parâmetros:
    - channel_langs (np.ndarray): Idiomas dos canais em formato string.
    - use_channel_lang (np.ndarray): Máscara booleana indicando se deve usar o idioma do canal.
    - languages (np.ndarray): Lista de idiomas disponíveis.
    - rng (np.random.Generator): Gerador de números aleatórios.

    Retorno:
    - np.ndarray: Idiomas finais atribuídos ao conteúdo.
    """
    random_langs = rng.choice(languages, size=len(channel_langs))
    first_langs = np.char.partition(channel_langs.astype(str), ',')[:, 0]
    return np.where(use_channel_lang, first_langs, random_langs)

def create_random_content(
    channels: pd.DataFrame,
    categories: np.ndarray,
    content_ratio: float,
    initial_id: int,
    current_date: float
) -> dict:
    """
    Gera conteúdos sintéticos com base em canais fornecidos, utilizando funções otimizadas para gerar
    IDs, títulos, status, categorias, idiomas, métricas, hashes e tipos específicos como vídeos, lives e shorts.

    Parâmetros:
    - channels (pd.DataFrame): DataFrame com os canais existentes.
    - categories (np.ndarray): Array com as categorias possíveis.
    - content_ratio (float): Proporção de canais a serem usados para gerar conteúdo.
    - initial_id (int): ID inicial para o conteúdo.
    - current_date (float): Timestamp (float) representando a data de criação do conteúdo.

    Retorno:
    - dict: Dicionário com os DataFrames gerados (conteúdo, tags, vídeos, lives, etc.) e métricas de tempo.
    """
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
    content_title = np.char.add(channel_names, ' Content ' + str(current_date))
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
    content_category = np.where(use_channel_cat, channel_categories, rng.choice(categories, size=num_content)).astype(np.int8)
    timings['category'] = time.perf_counter() - t1

    # Tags
    t1 = time.perf_counter()
    extra_tags = rng.integers(1, 16, size=num_content*2, dtype=np.int8)
    timings['tags_rng'] = time.perf_counter() - t1
    t1 = time.perf_counter()
    content_tags_array, content_tags_indexes = generate_tags_fast(content_category, extra_tags)
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
    df_CONTENT = pd.DataFrame({
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
    df_content_table = pd.DataFrame(
        np.column_stack((content_id, content_view_count, content_like_count, content_dislike_count, content_comment_count)),
        columns=["ContentID", "Views", "Likes", "Dislikes", "Comments"]
    )

    timings['CONTENT'] = time.perf_counter() - t1
    
    t1 = time.perf_counter()
    # Tags
    # Pré-processamento
    cid_subset = content_id.astype(np.int32)

    # Chamada Cython
    tag_rows = generate_content_tags(cid_subset, content_tags_array, content_tags_indexes)

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
    