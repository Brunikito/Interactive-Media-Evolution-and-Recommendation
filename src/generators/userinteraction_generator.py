"""
Module: user_interaction_generator
----------------------------------

Este módulo gera interações sintéticas de usuários com conteúdos (como likes, dislikes ou neutras),
baseando-se em usuários que estão atualmente assistindo conteúdo (`UIsWatchingCONTNow`).

Ele verifica quais usuários ainda **não interagiram** com os conteúdos que estão assistindo
e gera novas interações para uma fração deles, definida por `interaction_ratio`.

Dependências:
- Dados de usuários assistindo conteúdo (`UWATCHINGCONT.parquet`)
- Tabelas de interações (`USERINTERACTION.csv`, `UCONTINT.csv`)
- NumPy para amostragem aleatória vetorial
"""

import pandas as pd
import numpy as np
import os
import time
from src import BASE_PATH, DATA_PATH

def create_random_user_interactions(
    interaction_ratio: float,
    uwatchingcont: pd.DataFrame,
    userinteraction: pd.DataFrame,
    ucontint: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Gera interações sintéticas (like, dislike, neutro) entre usuários e conteúdos que estão assistindo,
    considerando apenas os casos onde ainda não houve interação registrada.

    Parâmetros:
    - interaction_ratio (float): Proporção de usuários assistindo que devem interagir com os conteúdos.
    - uwatchingcont (pd.DataFrame): DataFrame com usuários assistindo conteúdos no momento.
    - userinteraction (pd.DataFrame): Interações de usuário existentes (UINTID, UserID, UINTType).
    - ucontint (pd.DataFrame): Mapeamento entre interações e conteúdos (UINTID, ContentID).

    Retorno:
    - tuple de pd.DataFrame:
        - userinteraction: Novas interações de usuários (com tipo e ID).
        - ucontint: Novas associações entre interações e conteúdos.
    """
    if uwatchingcont.shape[0] < 10:
        userinteraction = pd.DataFrame(columns=[
            'UINTType',
            'UINTID',
            'UserID',
            ])

        ucontint = pd.DataFrame(columns=[
            'UINTID',
            'ContentID',
            ])
        
        return userinteraction, ucontint
    
    total_start = time.time()

    # 1. Filtrar usuários que estão assistindo agora
    t1 = time.time()
    now_watching = uwatchingcont[uwatchingcont['UIsWatchingCONTNow']]
    t2 = time.time()

    # 2. Juntar interações já existentes
    content_interactions = pd.merge(ucontint, userinteraction, how='left')
    content_interactions = content_interactions[content_interactions['UINTType'] != 0]
    t3 = time.time()
    
    columns_needed = ['UserID', 'ContentID']  # ou outras que você usa
    filtered = now_watching[columns_needed]
    
    # Faz merge e identifica quem não tem interação ainda
    merged = filtered.merge(
        content_interactions[['UserID', 'ContentID']],
        on=['UserID', 'ContentID'],
        how='left',
        indicator=True
    )

    # Filtra os que não têm correspondência (i.e. não interagiram)
    now_watching_no_int = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    t4 = time.time()

    # 4. Amostrar usuários para gerar interação
    rng = np.random.default_rng()
    num_interactions = int(now_watching_no_int.shape[0] * interaction_ratio)
    filtered = now_watching_no_int[columns_needed]
    positions = rng.choice(len(filtered), size=num_interactions, replace=False)
    now_watchin_interactions = filtered.iloc[positions]
    t5 = time.time()

    # 5. Gerar arrays de interações
    user_ids = now_watchin_interactions['UserID'].values.astype(np.int32)
    content_ids = now_watchin_interactions['ContentID'].values.astype(np.int32)
    likes_dislikes = rng.choice((-1, 0, 1), num_interactions, replace=True, p=(0.3, 0.2, 0.5)).astype(np.int8)
    interaction_ids = np.arange(userinteraction.shape[0], userinteraction.shape[0] + num_interactions, dtype=np.int32)
    t6 = time.time()

    # 6. Criar novos DataFrames
    userinteraction = pd.DataFrame({
        'UINTType': likes_dislikes,
        'UINTID': interaction_ids,
        'UserID': user_ids,
    })

    ucontint = pd.DataFrame({
        'UINTID': interaction_ids,
        'ContentID': content_ids,
    })
    t7 = time.time()

    # 7. Imprimir tempos
    print("\n⏱️ Tempos por etapa:")
    print(f"1. Filtrar watching atual:       {t2 - t1:.4f}s")
    print(f"2. Merge com interações:         {t3 - t2:.4f}s")
    print(f"3. Remover quem já interagiu:    {t4 - t3:.4f}s")
    print(f"4. Sample de interações novas:   {t5 - t4:.4f}s")
    print(f"5. Gerar arrays e IDs:           {t6 - t5:.4f}s")
    print(f"6. Criar DataFrames finais:      {t7 - t6:.4f}s")
    print(f"🧮 Tempo total:                  {t7 - total_start:.4f}s\n")

    return userinteraction, ucontint

if __name__ == '__main__':
    import time
    interaction_ratio = 1
    uwatchingcont = pd.read_parquet(os.path.join(BASE_PATH, 'UWATCHINGCONT.parquet'))
    userinteraction = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'USERINTERACTION.csv'))
    ucontint = pd.read_csv(os.path.join(DATA_PATH, 'tables', 'UCONTINT.csv'))
    print('Executando...')
    init_timer = time.time()
    uint_df, ucontint_df = create_random_user_interactions(interaction_ratio, uwatchingcont, userinteraction, ucontint)
    print(f'Executado em: {time.time() - init_timer :.6f}s')
