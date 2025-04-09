import pandas as pd
import numpy as np
from src.generators.cython.cy_channel_generator import create_random_channel
from src.generators.feature_generators.channel_name_generator import generate_channel_name
from src import BASE_PATH
import os

if __name__ == "__main__":
    import timeit
    path = os.path.join(BASE_PATH, "usuarios_full.parquet")
    print(path)
    users = pd.read_parquet(path)
    print("Total de usuários:", len(users))
    print("Usuários sem canal:", users['user_channel_id'].isna().sum())
    # Gerando os canais
    print("Criando canais aleatórios...")
    start_time = timeit.default_timer()
    users, channels = create_random_channel(users, 1, 0, 0, generate_channel_name)
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print("Canais criados e salvos.")
    print(f"Tempo decorrido: {elapsed_time:.2f} segundos")
    print("Uso de memória:")
    print(users.memory_usage().sum() / (1024 ** 2), "MB")
    print(channels.memory_usage().sum() / (1024 ** 2), "MB")
    # Imprimindo as primeiras linhas dos canais
    print("Canais gerados")
    print("Salvando canais...")
    users.to_parquet(os.path.join(BASE_PATH, "usuarios_full_chCreate.parquet"), index=False)
    channels.to_parquet(os.path.join(BASE_PATH, "channels_full.parquet"), index=False)
    print("Canais salvos.")