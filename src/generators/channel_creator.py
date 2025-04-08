import pandas as pd
import numpy as np
from .cython.cy_channel_generator import create_random_channel
from .feature_generators.channel_name_generator import generate_channel_name
from src import BASE_PATH
import os

if __name__ == "__main__":
    path = os.path.join(BASE_PATH, "usuarios_full.parquet")
    print(path)
    users = pd.read_parquet(path)
    print("Total de usuários:", len(users))
    print("Usuários sem canal:", users['user_channel_id'].isna().sum())
    # Gerando os canais
    users, channels = create_random_channel(users, 1, 0, 0, generate_channel_name)

    # Imprimindo as primeiras linhas dos canais
    print("Canais gerados:")
    print(channels.shape)
    print(channels.head(10))
