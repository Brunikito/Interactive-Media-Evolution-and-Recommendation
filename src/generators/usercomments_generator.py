"""
Module: comment_generator
-------------------------

Este módulo gera comentários sintéticos com base em usuários que estão assistindo conteúdos no momento. 
Distribui os comentários entre conteúdos do tipo Live, Vídeo e Short, e também cria respostas (replies) 
para comentários existentes de maneira randômica, seguindo uma lógica proporcional (`comment_ratio`).

O processo inclui:
- Filtragem de usuários assistindo
- Sorteio de conteúdo e comentários
- Criação de novos comentários e respostas
- Separação por tipo de conteúdo

Dependências:
- pandas, numpy
- Arquivos de conteúdo (`LIVE.parquet`, `VIDEO.parquet`, `SHORT.parquet`)
- Comentários existentes (`COMMENT.csv`, etc.)
"""

import pandas as pd
import numpy as np
import time

def create_random_comments(
    comment_ratio: float,
    uwatchingcont: pd.DataFrame,
    comments: pd.DataFrame,
    livecomments: pd.DataFrame,
    videocomments: pd.DataFrame,
    shortcomments: pd.DataFrame,
    current_datetime: float,
    lives: pd.DataFrame,
    videos: pd.DataFrame,
    shorts: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Gera comentários sintéticos com base em usuários assistindo conteúdos, com possibilidade de
    gerar comentários originais ou respostas a comentários existentes, distribuídos entre tipos de conteúdo.

    Parâmetros:
    - comment_ratio (float): Proporção de usuários assistindo que devem comentar.
    - uwatchingcont (pd.DataFrame): DataFrame com usuários assistindo conteúdos no momento.
    - comments (pd.DataFrame): Comentários já existentes (base principal).
    - livecomments, videocomments, shortcomments (pd.DataFrame): Comentários já existentes por tipo de conteúdo.
    - current_datetime (float): Timestamp atual da simulação.
    - lives, videos, shorts (pd.DataFrame): Tabelas de conteúdo do tipo Live, Vídeo e Short.

    Retorno:
    - tuple de pd.DataFrames:
        - new_comments: DataFrame com os novos comentários.
        - new_replies: DataFrame com mapeamentos de respostas.
        - new_live_comments: Comentários para conteúdos ao vivo.
        - new_video_comments: Comentários para vídeos.
        - new_short_comments: Comentários para shorts.
    """

    t0 = time.time()
    rng = np.random.default_rng()
    
    # 1. Filtrar usuários assistindo agora
    watching_now = uwatchingcont[uwatchingcont['UIsWatchingCONTNow']].copy()
    num_comments = int(len(watching_now) * comment_ratio)

    t1 = time.time()

    if num_comments == 0:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Content types merge
    content_ids = pd.concat([
        lives['ContentID'], 
        videos['ContentID'], 
        shorts['ContentID']
    ], ignore_index=True)

    content_types = pd.DataFrame({
        'ContentID': content_ids,
        'Type': np.repeat([0, 1, 2], [
            lives.shape[0], videos.shape[0], shorts.shape[0]
        ]).astype(np.int8)
    })
    
    t21 = time.time()
    
    content_types = content_types.set_index('ContentID')
    watching_now_with_types = watching_now[['UserID', 'ContentID']].copy()
    watching_now_with_types['Type'] = content_types.loc[watching_now_with_types['ContentID']].values
    t2 = time.time()

    # Agrupamento e merge de comentários existentes
    content_comments = pd.concat(
        [livecomments[['ContentID', 'CommentID']],
        videocomments[['ContentID', 'CommentID']],
        shortcomments[['ContentID', 'CommentID']]],
        ignore_index=True
    )
    t31 = time.time()
    watching_now_ID = pd.DataFrame()
    watching_now_ID['ContentID'] = watching_now['ContentID']
    watching_now_comments = pd.merge(watching_now_ID, content_comments, on='ContentID', how='left')
    t32 = time.time()
    
    # Gargalo
    positions = rng.permutation(watching_now_comments.shape[0], axis=0)
    t33 = time.time()
    
    reply_choices = watching_now_comments.iloc[positions].drop_duplicates(subset='ContentID', keep='first').reset_index(drop=True)

    t3 = time.time()
    
    reply_choices['CommentID'] = reply_choices['CommentID'].fillna(np.int32(-1))
    reply_choices = reply_choices.set_index('ContentID')
    watching_now_with_types['CommentID'] = reply_choices.loc[watching_now_with_types['ContentID']].values
    
    t41 = time.time()
    
    positions = rng.permutation(watching_now_with_types.shape[0])
    chosen_lines = watching_now_with_types.iloc[positions[:num_comments]]

    t4 = time.time()

    chosen_lines_mandatory_content = chosen_lines[chosen_lines['CommentID'] == -1][['UserID', 'ContentID', 'Type']].reset_index(drop=True)
    chosen_lines_content_or_comentary = chosen_lines[chosen_lines['CommentID'] != -1].reset_index(drop=True)

    if chosen_lines_content_or_comentary.empty:
        total_chosen_content = chosen_lines_mandatory_content.copy()
        replies = pd.DataFrame(columns=['UserID', 'CommentID'])
        ids = []
        total_lines = 0
    else:
        total_lines = chosen_lines_content_or_comentary.shape[0]
        half_lines = total_lines // 2
        ids = rng.permutation(total_lines, axis=0).astype(np.int32)

        lines_content = chosen_lines_content_or_comentary.iloc[ids[:half_lines]].reset_index(drop=True)
        lines_content = lines_content[['UserID', 'ContentID', 'Type']]
        total_chosen_content = pd.concat((chosen_lines_mandatory_content, lines_content), axis=0, ignore_index=True)

        lines_comment = chosen_lines_content_or_comentary.iloc[ids[half_lines:]].reset_index(drop=True)
        replies = lines_comment[['UserID', 'CommentID']]

    t5 = time.time()

    new_comments_id = rng.permutation(np.arange(
        comments.shape[0],
        comments.shape[0] + total_chosen_content.shape[0] + replies.shape[0]
    ), axis=0)

    content_coments_new_id = new_comments_id[:total_chosen_content.shape[0]]
    replies_new_id = new_comments_id[total_chosen_content.shape[0]:]
    total_chosen_content['CommentID'] = content_coments_new_id
    total_lines = total_chosen_content.shape[0] + replies.shape[0]

    replies = replies.copy()
    replies['COMisRepByCOMCommentID'] = replies_new_id

    all_user_ids = pd.concat([total_chosen_content['UserID'], replies['UserID']], ignore_index=True).astype(np.int32)

    new_comments = pd.DataFrame({
        'CommentID': new_comments_id,
        'COMDateTime': np.full(total_lines, current_datetime, dtype=np.float32),
        'COMisEdited': np.zeros(total_lines, dtype=np.bool_),
        'COMBody': np.zeros(total_lines, dtype=np.bool_),
        'UserID': all_user_ids
    })

    t6 = time.time()

    new_replies = replies[['CommentID', 'COMisRepByCOMCommentID']]
    new_live_comments = total_chosen_content[total_chosen_content['Type'] == 0][['CommentID', 'ContentID']]
    new_video_comments = total_chosen_content[total_chosen_content['Type'] == 1][['CommentID', 'ContentID']]
    new_short_comments = total_chosen_content[total_chosen_content['Type'] == 2][['CommentID', 'ContentID']]

    t7 = time.time()

    print("\n⏱️ Timers (em segundos):")
    print(f"▶️  t1 - leitura + filtro         : {t1 - t0:.4f}")
    print(f"▶️  t21 - concat conteúdos        : {t21 - t1:.4f}")
    print(f"▶️  t2 - merge tipos de conteúdo  : {t2 - t1:.4f}")
    print(f"▶️  t31 - concat comentários      : {t31 - t2:.4f}")
    print(f"▶️  t32 - merge comentários       : {t32 - t31:.4f}")
    print(f"▶️  t33 - sorteando o array       : {t33 - t32:.4f}")
    print(f"▶️  t3 - agrupamento comentários  : {t3 - t33:.4f}")
    print(f"▶️  t41 - merge final              : {t41 - t3:.4f}")
    print(f"▶️  t42 - Amostra                  : {t4 - t41:.4f}")
    print(f"▶️  t5 - separação + splits       : {t5 - t4:.4f}")
    print(f"▶️  t6 - criação DataFrame final  : {t6 - t5:.4f}")
    print(f"▶️  t7 - splits por tipo          : {t7 - t6:.4f}")
    print(f"⏳  Tempo total                   : {t7 - t0:.4f}\n")

    return new_comments, new_replies, new_live_comments, new_video_comments, new_short_comments

if __name__ == '__main__':
    import os
    from src import BASE_PATH, DATA_PATH, TABLES_PATH
    
    print('SETUP')
    initial_time = time.time()
    comment_ratio = 1
    uwatchingcont = pd.read_parquet(os.path.join(BASE_PATH, 'UWATCHINGCONT.parquet'))
    comments = pd.read_csv(os.path.join(TABLES_PATH, 'COMMENT.csv'))
    livecomments = pd.read_csv(os.path.join(TABLES_PATH, 'LIVECOMMENT.csv'))
    videocomments = pd.read_csv(os.path.join(TABLES_PATH, 'VIDEOCOMMENT.csv'))
    shortcomments = pd.read_csv(os.path.join(TABLES_PATH, 'SHORTCOMMENT.csv'))
    current_datetime = 0
    lives = pd.read_parquet(os.path.join(BASE_PATH, 'LIVE.parquet'))
    videos = pd.read_parquet(os.path.join(BASE_PATH, 'VIDEO.parquet'))
    shorts = pd.read_parquet(os.path.join(BASE_PATH, 'SHORT.parquet'))
    print(f'Elapsed Time: {time.time() - initial_time:.4f}s')
    
    
    print('Function')
    initial_time = time.time()
    new_comments, new_replies, new_live_comments, new_video_comments, new_short_comments = generate_random_comments(
        comment_ratio, uwatchingcont, comments,
        livecomments, videocomments, shortcomments, 
        current_datetime,
        lives, videos, shorts
        )
    print(f'Elapsed Time: {time.time() - initial_time:.4f}s')
    
    print(new_comments.head(3))
    print(new_comments.shape)
    print(new_replies.head(3))
    print(new_live_comments.head(3))
    print(new_video_comments.head(3))
    print(new_short_comments.head(3))
    
    print(f'Total comments: {new_comments.shape[0]}')
    