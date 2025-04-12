"""
Module: create_random_channel_py
--------------------------------

Este módulo define um wrapper em Python para a função `create_random_channel`, 
ligando-a à função `generate_channel_name`. Serve como um ponto de integração 
entre a lógica de criação de canais (possivelmente acelerada com Cython) 
e a geração de nomes de canais.

A função recebe um DataFrame de usuários e outros parâmetros de controle, 
e retorna os canais criados, os usuários atualizados e a tabela `CHANNEL` no formato compatível com o sistema.

Dependências:
- create_random_channel: Lógica central de criação de canais.
- generate_channel_name: Geração de nomes aleatórios ou únicos para canais.
"""

from src.generators.cython.cy_channel_generator import create_random_channel
from src.generators.feature_generators.channel_name_generator import generate_channel_name
import pandas as pd

def create_random_channel_py(
    users: pd.DataFrame,
    new_channel_ratio: float,
    initial_id: int,
    current_date_time: float
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Cria canais aleatórios utilizando um DataFrame de usuários e metadados fornecidos,
    e atribui nomes gerados automaticamente via `generate_channel_name`.

    Parâmetros:
    - users (pandas.DataFrame): DataFrame contendo os usuários que poderão criar canais.
    - new_channel_ratio (float): Proporção de usuários que devem criar novos canais.
    - initial_id (int): ID inicial para os canais criados.
    - current_date_time (float): Timestamp atual (como float) para marcar a criação.

    Retorno:
    - tuple:
        - users (pandas.DataFrame): DataFrame de usuários atualizado com informações de canal.
        - channels (pandas.DataFrame): DataFrame com os canais criados em formato analítico.
        - CHANNEL (pandas.DataFrame): DataFrame no formato compatível com a tabela de banco `CHANNEL`.
    """
    return create_random_channel(users, new_channel_ratio, initial_id, current_date_time, generate_channel_name)