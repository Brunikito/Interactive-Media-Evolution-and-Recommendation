import pandas as pd
import numpy as np
import time

from src import BASE_PATH, DATA_PATH, TABLES_PATH
from src.initialization.initialize_tables import initialize_tables, TABLE_PATHS
# Paths to tables

from src.iteration.cython.fast_concat import (
        concat_int8, concat_int16, concat_int32,
        concat_int64, concat_float32, concat_float64
    )
def clever_concat(arr1, arr2):
    #return np.concatenate((arr1, arr2), axis=0)
    if len(arr1) < 2_000_000 or len(arr2) < 2_000_000:
        return np.concatenate((arr1, arr2), axis=0)
    if isinstance(arr1, pd.Categorical) or isinstance(arr2, pd.Categorical):
        return np.concatenate((arr1, arr2), axis=0)
    match arr1.dtype:
        case 'int8':
            print('int8')
            return concat_int8(arr1, arr2)
        case 'int16':
            print('int16')
            return concat_int16(arr1, arr2)
        case 'int32':
            print('int32')
            return concat_int32(arr1, arr2)
        case 'int64':
            print('int64')
            return concat_int64(arr1, arr2)
        case 'float32':
            print('float32')
            return concat_float32(arr1, arr2)
        case 'float64':
            print('float64')
            return concat_float64(arr1, arr2)
        case _:
            return np.concatenate((arr1, arr2), axis=0)


def safe_concat(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    if df2.empty:
        return df1
    if df1.empty:
        return df2
    return fast_concat_same_columns(df1, df2)

GLOBAL_CONCAT_TIME = 0.0
GLOBAL_DF_TIME = 0.0

def fast_concat_same_columns(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Concatena dois DataFrames com colunas idênticas de forma eficiente,
    preservando a ordem e os dtypes de cada coluna.

    Assumptions:
    - df1 e df2 têm as mesmas colunas na mesma ordem.
    - Os tipos de dados por coluna são compatíveis.
    """
    global GLOBAL_CONCAT_TIME, GLOBAL_DF_TIME

    start = time.time()
    data = {
        col: clever_concat(df1[col].values, df2[col].values)
        for col in df1.columns
    }
    GLOBAL_CONCAT_TIME += time.time() - start
    
    start = time.time()
    df = pd.DataFrame(data)
    GLOBAL_DF_TIME += time.time() - start
    
    return df


def update_uwatching_cont(uwatchingcont, current_date_time):
    uwatchingcont_new = uwatchingcont.copy()
    uwatchingcont_new['UIsWatchingCONTNow'] = current_date_time < (uwatchingcont['UWatchCONTDateTime'] + uwatchingcont['UWatchDurationCONT'])
    return uwatchingcont_new

def load_all_tables(table_paths: dict) -> dict:
    """
    Lê todos os arquivos .parquet definidos no dicionário table_paths.

    Parâmetros:
    - table_paths (dict): Dicionário com nomes lógicos como chave e caminhos para arquivos .parquet como valor.

    Retorno:
    - dict: Dicionário com os mesmos nomes como chave e os DataFrames carregados como valor.
    """
    return {name: pd.read_parquet(path) for name, path in table_paths.items()}

def iterate(num_iterations: int, time_between_checks: float, initial_time: float, first_iteration: bool = True):
    # Inicializa os arquivos e carrega os caminhos
    print('Initializing')
    timer = time.time()
    
    if first_iteration:
        initialize_tables()
        
    # Imports
    from src.generators.content_generator import create_random_content
    from src.generators.user_generator import create_random_user
    from src.generators.channel_generator import create_random_channel_py
    from src.generators.uwatchingcont_generator import create_random_uwatching_cont
    from src.generators.usercomments_generator import create_random_comments
    from src.generators.userinteraction_generator import create_random_user_interactions
    
    # Lê todos os parquets
    tables = load_all_tables(TABLE_PATHS)

    # Desempacotar os DataFrames no escopo da função
    dataframes = {
        "users": tables["users"],
        "channels": tables["channels"],
        "content": tables["content"],
        "comments": tables["comments"],
        "USER": tables["USER"],
        "CHANNEL": tables["CHANNEL"],
        "UADMINCH": tables["UADMINCH"],
        "UINTERESTCH": tables["UINTERESTCH"],
        "CONTENT": tables["CONTENT"],
        "UWATCHINGCONT": tables["UWATCHINGCONT"],
        "LIVE": tables["LIVE"],
        "VIDEO": tables["VIDEO"],
        "SHORT": tables["SHORT"],
        "COMMENT": tables["COMMENT"],
        "LIVECOMMENT": tables["LIVECOMMENT"],
        "COMMENTREPLY": tables["COMMENTREPLY"],
        "VIDEOCOMMENT": tables["VIDEOCOMMENT"],
        "POLLCOMMENT": tables["POLLCOMMENT"],
        "SHORTCOMMENT": tables["SHORTCOMMENT"],
        "POLL": tables["POLL"],
        "PLAYLIST": tables["PLAYLIST"],
        "PLAYLISTCONTENT": tables["PLAYLISTCONTENT"],
        "USERINTERACTION": tables["USERINTERACTION"],
        "UCONTINT": tables["UCONTINT"],
        "UCOMINT": tables["UCOMINT"],
        "UPLAYINT": tables["UPLAYINT"],
        "NOTIFICATION": tables["NOTIFICATION"],
        "USERNOTIFIED": tables["USERNOTIFIED"],
        "CHANNEL_CHExtLink": tables["CHANNEL_CHExtLink"],
        "CONTENT_CONTTag": tables["CONTENT_CONTTag"],
        "PLAYLIST_PLAYTag": tables["PLAYLIST_PLAYTag"],
    }
    
    # Criar cópias iniciais para os DataFrames _new
    dataframes_new = {key: df.copy() for key, df in dataframes.items()}
    
    current_datetime = initial_time
    decay_rate = 0.001
    num_recommendations = 3
    comment_ratio = 0.4
    interact_ratio = 0.3
    prev_day_number = -1
    
    print(f'Finished Initialization in {time.time() - timer}')

    operations_timer = 0
    concat_timer = 0
    copy_timer = 0
    
    for i in range(num_iterations):
        timer = time.time()
        day_number = current_datetime // 86400
        if prev_day_number != day_number:
            prev_day_number = day_number
            print(f'Current Datetime: Day{day_number}, {(current_datetime // 3600) % 24:02.0f}h{(current_datetime // 60) % 60:02.0f}min, {current_datetime % 60:02.0f}sec')
        
        # Operações de geração de dados
        dataframes["users"], dataframes["USER"] = create_random_user(
            2_000_000,
            dataframes["users"].shape[0]
        )
        dataframes["users"], dataframes["channels"], dataframes["CHANNEL"] = create_random_channel_py(
            dataframes["users"], np.exp(-decay_rate * i), dataframes["channels"].shape[0], current_datetime
        )
        content_dict = create_random_content(
            dataframes["channels"], np.arange(1, 16, dtype=np.int8), np.exp(-decay_rate * i),
            dataframes["content"].shape[0], current_datetime
        )
        dataframes["content"] = content_dict['df_content']
        dataframes["CONTENT"] = content_dict['df_CONTENT']
        dataframes["CONTENT_CONTTag"] = content_dict['df_content_tag']
        dataframes["VIDEO"] = content_dict['df_video']
        dataframes["SHORT"] = content_dict['df_short']
        dataframes["LIVE"] = content_dict['df_live']
        dataframes["UWATCHINGCONT"] = create_random_uwatching_cont(
            0.1, dataframes["users"], dataframes["USER"], dataframes["content"], dataframes["CONTENT"],
            dataframes["UWATCHINGCONT"], dataframes["CONTENT_CONTTag"], 
            dataframes["USERINTERACTION"], dataframes["UCONTINT"], dataframes["COMMENT"], 
            dataframes["LIVECOMMENT"], dataframes["VIDEOCOMMENT"], dataframes["SHORTCOMMENT"],
            num_recommendations, current_datetime
        )
        (dataframes["COMMENT"], dataframes["COMMENTREPLY"], dataframes["LIVECOMMENT"],
         dataframes["VIDEOCOMMENT"], dataframes["SHORTCOMMENT"]) = create_random_comments(
            comment_ratio, dataframes["UWATCHINGCONT"], dataframes["COMMENT"],
            dataframes["LIVECOMMENT"], dataframes["VIDEOCOMMENT"], dataframes["SHORTCOMMENT"],
            current_datetime, dataframes["LIVE"], dataframes["VIDEO"], dataframes["SHORT"]
        )
        dataframes["USERINTERACTION"], dataframes["UCONTINT"] = create_random_user_interactions(
            interact_ratio, dataframes["UWATCHINGCONT"], 
            dataframes["USERINTERACTION"], dataframes["UCONTINT"]
        )
        current_datetime += time_between_checks
        dataframes["UWATCHINGCONT"] = update_uwatching_cont(dataframes["UWATCHINGCONT"], current_datetime)
        
        operations_timer += time.time() - timer
        timer = time.time()
        
        # Concatenar todos os DataFrames
        for key in dataframes:
            dataframes_new[key] = safe_concat(dataframes_new[key], dataframes[key])
        
        concat_timer += time.time() - timer
        timer = time.time()
        
        # Atualizar os DataFrames originais com os concatenados
        dataframes.update(dataframes_new)
        
        copy_timer += time.time() - timer
    
    print(f'Operations Time: {operations_timer}s')
    print(f'Concat Time: {concat_timer}s')
    print(f'Copy Timer: {copy_timer}s')
    
    print('Updating Tables')
    tables.update(dataframes_new)
    print('Tables Updated')
    
    print('Start Saving')
    for name, df in tables.items():
        df.to_parquet(TABLE_PATHS[name], index=False)
    print('End Saving')
    return

from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"⏱️ Iniciando '{func.__name__}'...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"✅ '{func.__name__}' finalizado em {duration} segundos")
        return result
    return wrapper


if __name__ == '__main__':
    '''
    size = 1_000_000
    
    print('Generating arrays')
    timer = time.time()
    arr1 = np.random.randint(0, 12111, size=size, dtype=np.int16)
    arr2 = np.random.randint(0, 12111, size=size, dtype=np.int16)
    end_time = time.time() - timer
    print(f'Generate 2 arrays with size {size} in {end_time}s')
    @timeit
    def concat_numpy(arr1, arr2):
        return np.concatenate((arr1, arr2), axis=0)
    @timeit
    def concat_int_concat(arr1, arr2):
        return concat_int16(arr1, arr2)
    @timeit
    def concat_clever_concat(arr1, arr2):
        return clever_concat(arr1, arr2)
    
    teste_1 = concat_numpy(arr1, arr2)
    teste_2 = concat_int_concat(arr1, arr2)
    teste_3 = concat_clever_concat(arr1, arr2)
    
    print(arr1.dtype)
    print(arr2.dtype)
    '''
        
    @timeit
    def run_simulation5():
        iterate(5, 60, 0, False)
        
    run_simulation5()
    print(GLOBAL_CONCAT_TIME)
    print(GLOBAL_DF_TIME)
    
    '''
    @timeit
    def run_simulation200():
        iterate(200, 60, 0, True)
    run_simulation200()
    print(GLOBAL_CONCAT_TIME)
    print(GLOBAL_DF_TIME)
    '''