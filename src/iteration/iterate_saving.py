import pandas as pd
import numpy as np
import time

from src import BASE_PATH, DATA_PATH, TABLES_PATH
from src.initialization.initialize_tables import initialize_tables, TABLE_PATHS
# Paths to tables

def safe_concat(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """
    Concatena dois DataFrames de forma eficiente, lidando com colunas comuns.
    """
    if df2.empty:
        return df1
    if df1.empty:
        return df2

    # Identifica colunas comuns rapidamente
    common_cols = df1.columns.intersection(df2.columns)
    if not common_cols.size:
        return df1

    # Remove colunas completamente NaN de df2 e alinha
    df2_clean = df2[common_cols].dropna(axis=1, how='all')
    if df2_clean.empty:
        return df1

    # Concatena diretamente com colunas alinhadas
    return pd.concat([df1[common_cols], df2_clean], ignore_index=True, copy=False)

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
    users = tables["users"]
    channels = tables["channels"]
    content = tables["content"]
    comments = tables["comments"]

    USER = tables["USER"]
    CHANNEL = tables["CHANNEL"]
    UADMINCH = tables["UADMINCH"]
    UINTERESTCH = tables["UINTERESTCH"]
    CONTENT = tables["CONTENT"]
    UWATCHINGCONT = tables["UWATCHINGCONT"]
    LIVE = tables["LIVE"]
    VIDEO = tables["VIDEO"]
    SHORT = tables["SHORT"]
    COMMENT = tables["COMMENT"]
    LIVECOMMENT = tables["LIVECOMMENT"]
    COMMENTREPLY = tables["COMMENTREPLY"]
    VIDEOCOMMENT = tables["VIDEOCOMMENT"]
    POLLCOMMENT = tables["POLLCOMMENT"]
    SHORTCOMMENT = tables["SHORTCOMMENT"]
    POLL = tables["POLL"]
    PLAYLIST = tables["PLAYLIST"]
    PLAYLISTCONTENT = tables["PLAYLISTCONTENT"]
    USERINTERACTION = tables["USERINTERACTION"]
    UCONTINT = tables["UCONTINT"]
    UCOMINT = tables["UCOMINT"]
    UPLAYINT = tables["UPLAYINT"]
    NOTIFICATION = tables["NOTIFICATION"]
    USERNOTIFIED = tables["USERNOTIFIED"]
    CHANNEL_CHExtLink = tables["CHANNEL_CHExtLink"]
    CONTENT_CONTTag = tables["CONTENT_CONTTag"]
    PLAYLIST_PLAYTag = tables["PLAYLIST_PLAYTag"]
    
    
    users_new = users.copy()
    channels_new = channels.copy()
    content_new = content.copy()
    comments_new = comments.copy()
    
    USER_new = USER.copy()
    CHANNEL_new = CHANNEL.copy()
    UADMINCH_new = UADMINCH.copy()
    UINTERESTCH_new = UINTERESTCH.copy()
    CONTENT_new = CONTENT.copy()
    UWATCHINGCONT_new = UWATCHINGCONT.copy()
    LIVE_new = LIVE.copy()
    VIDEO_new = VIDEO.copy()
    SHORT_new = SHORT.copy()
    COMMENT_new = COMMENT.copy()
    LIVECOMMENT_new = LIVECOMMENT.copy()
    COMMENTREPLY_new = COMMENTREPLY.copy()
    VIDEOCOMMENT_new = VIDEOCOMMENT.copy()
    POLLCOMMENT_new = POLLCOMMENT.copy()
    SHORTCOMMENT_new = SHORTCOMMENT.copy()
    POLL_new = POLL.copy()
    PLAYLIST_new = PLAYLIST.copy()
    PLAYLISTCONTENT_new = PLAYLISTCONTENT.copy()
    USERINTERACTION_new = USERINTERACTION.copy()
    UCONTINT_new = UCONTINT.copy()
    UCOMINT_new = UCOMINT.copy()
    UPLAYINT_new = UPLAYINT.copy()
    NOTIFICATION_new = NOTIFICATION.copy()
    USERNOTIFIED_new = USERNOTIFIED.copy()
    CHANNEL_CHExtLink_new = CHANNEL_CHExtLink.copy()
    CONTENT_CONTTag_new = CONTENT_CONTTag.copy()
    PLAYLIST_PLAYTag_new = PLAYLIST_PLAYTag.copy()
    
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
        users, USER = create_random_user(int(users.shape[0]*0.001 + (current_datetime//3600) + 5*np.exp(-decay_rate * i)), users.shape[0])
        users, channels, CHANNEL = create_random_channel_py(users, np.exp(-decay_rate * i), channels.shape[0], current_datetime)
        content_dict = create_random_content(channels, np.arange(1, 16, dtype=np.int8), np.exp(-decay_rate * i), content.shape[0], current_datetime)
        content = content_dict['df_content']
        CONTENT = content_dict['df_CONTENT']
        CONTENT_CONTTag = content_dict['df_content_tag']
        VIDEO = content_dict['df_video']
        SHORT = content_dict['df_short']
        LIVE = content_dict['df_live']
        UWATCHINGCONT = create_random_uwatching_cont(
            0.1, users, USER, content, CONTENT,
            UWATCHINGCONT, CONTENT_CONTTag, 
            USERINTERACTION, UCONTINT, COMMENT, 
            LIVECOMMENT, VIDEOCOMMENT, SHORTCOMMENT,
            num_recommendations, current_datetime
            )
        COMMENT, COMMENTREPLY, LIVECOMMENT, VIDEOCOMMENT, SHORTCOMMENT = create_random_comments(
            comment_ratio, UWATCHINGCONT, COMMENT,
            LIVECOMMENT, VIDEOCOMMENT, SHORTCOMMENT,
            current_datetime, LIVE, VIDEO, SHORT
        )
        USERINTERACTION, UCONTINT = create_random_user_interactions(
            interact_ratio, UWATCHINGCONT, 
            USERINTERACTION, UCONTINT
        )
        current_datetime += time_between_checks
        UWATCHINGCONT = update_uwatching_cont(UWATCHINGCONT, current_datetime)
        
        operations_timer += time.time() - timer
        timer = time.time()
        
        users_new = safe_concat(users_new, users)
        channels_new = safe_concat(channels_new, channels)
        content_new = safe_concat(content_new, content)
        comments_new = safe_concat(comments_new, comments)
        
        USER_new = safe_concat(USER_new, USER)
        CHANNEL_new = safe_concat(CHANNEL_new, CHANNEL)
        UADMINCH_new = safe_concat(UADMINCH_new, UADMINCH)
        UINTERESTCH_new = safe_concat(UINTERESTCH_new, UINTERESTCH)
        CONTENT_new = safe_concat(CONTENT_new, CONTENT)
        UWATCHINGCONT_new = safe_concat(UWATCHINGCONT_new, UWATCHINGCONT)
        LIVE_new = safe_concat(LIVE_new, LIVE)
        VIDEO_new = safe_concat(VIDEO_new, VIDEO)
        SHORT_new = safe_concat(SHORT_new, SHORT)
        COMMENT_new = safe_concat(COMMENT_new, COMMENT)
        LIVECOMMENT_new = safe_concat(LIVECOMMENT_new, LIVECOMMENT)
        COMMENTREPLY_new = safe_concat(COMMENTREPLY_new, COMMENTREPLY)
        VIDEOCOMMENT_new = safe_concat(VIDEOCOMMENT_new, VIDEOCOMMENT)
        POLLCOMMENT_new = safe_concat(POLLCOMMENT_new, POLLCOMMENT)
        SHORTCOMMENT_new = safe_concat(SHORTCOMMENT_new, SHORTCOMMENT)
        POLL_new = safe_concat(POLL_new, POLL)
        PLAYLIST_new = safe_concat(PLAYLIST_new, PLAYLIST)
        PLAYLISTCONTENT_new = safe_concat(PLAYLISTCONTENT_new, PLAYLISTCONTENT)
        USERINTERACTION_new = safe_concat(USERINTERACTION_new, USERINTERACTION)
        UCONTINT_new = safe_concat(UCONTINT_new, UCONTINT)
        UCOMINT_new = safe_concat(UCOMINT_new, UCOMINT)
        UPLAYINT_new = safe_concat(UPLAYINT_new, UPLAYINT)
        NOTIFICATION_new = safe_concat(NOTIFICATION_new, NOTIFICATION)
        USERNOTIFIED_new = safe_concat(USERNOTIFIED_new, USERNOTIFIED)
        CHANNEL_CHExtLink_new = safe_concat(CHANNEL_CHExtLink_new, CHANNEL_CHExtLink)
        CONTENT_CONTTag_new = safe_concat(CONTENT_CONTTag_new, CONTENT_CONTTag)
        PLAYLIST_PLAYTag_new = safe_concat(PLAYLIST_PLAYTag_new, PLAYLIST_PLAYTag)
    
        concat_timer += time.time() - timer
        timer = time.time()
        
        users = users_new
        channels = channels_new
        content = content_new
        comments = comments_new
        
        USER = USER_new
        CHANNEL = CHANNEL_new
        UADMINCH = UADMINCH_new
        UINTERESTCH = UINTERESTCH_new
        CONTENT = CONTENT_new
        UWATCHINGCONT = UWATCHINGCONT_new
        LIVE = LIVE_new
        VIDEO = VIDEO_new
        SHORT = SHORT_new
        COMMENT = COMMENT_new
        LIVECOMMENT = LIVECOMMENT_new
        COMMENTREPLY = COMMENTREPLY_new
        VIDEOCOMMENT = VIDEOCOMMENT_new
        POLLCOMMENT = POLLCOMMENT_new
        SHORTCOMMENT = SHORTCOMMENT_new
        POLL = POLL_new
        PLAYLIST = PLAYLIST_new
        PLAYLISTCONTENT = PLAYLISTCONTENT_new
        USERINTERACTION = USERINTERACTION_new
        UCONTINT = UCONTINT_new
        UCOMINT = UCOMINT_new
        UPLAYINT = UPLAYINT_new
        NOTIFICATION = NOTIFICATION_new
        USERNOTIFIED = USERNOTIFIED_new
        CHANNEL_CHExtLink = CHANNEL_CHExtLink_new
        CONTENT_CONTTag = CONTENT_CONTTag_new
        PLAYLIST_PLAYTag = PLAYLIST_PLAYTag_new
        
        copy_timer += time.time() - timer
    
    print(f'Operations Time: {operations_timer}s')
    print(f'Concat Time: {concat_timer}s')
    print(f'Copy Timer: {copy_timer}s')
    
    print('Updating Tables')
    tables.update({
            "users": users_new,
            "channels": channels_new,
            "content": content_new,
            "comments": comments_new,
            "USER": USER_new,
            "CHANNEL": CHANNEL_new,
            "UADMINCH": UADMINCH_new,
            "UINTERESTCH": UINTERESTCH_new,
            "CONTENT": CONTENT_new,
            "UWATCHINGCONT": UWATCHINGCONT_new,
            "LIVE": LIVE_new,
            "VIDEO": VIDEO_new,
            "SHORT": SHORT_new,
            "COMMENT": COMMENT_new,
            "LIVECOMMENT": LIVECOMMENT_new,
            "COMMENTREPLY": COMMENTREPLY_new,
            "VIDEOCOMMENT": VIDEOCOMMENT_new,
            "POLLCOMMENT": POLLCOMMENT_new,
            "SHORTCOMMENT": SHORTCOMMENT_new,
            "POLL": POLL_new,
            "PLAYLIST": PLAYLIST_new,
            "PLAYLISTCONTENT": PLAYLISTCONTENT_new,
            "USERINTERACTION": USERINTERACTION_new,
            "UCONTINT": UCONTINT_new,
            "UCOMINT": UCOMINT_new,
            "UPLAYINT": UPLAYINT_new,
            "NOTIFICATION": NOTIFICATION_new,
            "USERNOTIFIED": USERNOTIFIED_new,
            "CHANNEL_CHExtLink": CHANNEL_CHExtLink_new,
            "CONTENT_CONTTag": CONTENT_CONTTag_new,
            "PLAYLIST_PLAYTag": PLAYLIST_PLAYTag_new,
        })
    print('Tables Updated')
    # Salvar todos os DataFrames atualizados nos seus respectivos paths
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
        print(f"✅ '{func.__name__}' finalizado em {duration:.2f} segundos")
        return result
    return wrapper

if __name__ == '__main__':
    #@timeit
    def run_simulation20():
        iterate(20, 60, 0, True)
    
    #@timeit
    def run_simulation100():
        iterate(100, 60, 0, True)
        
    run_simulation20()
    run_simulation100()