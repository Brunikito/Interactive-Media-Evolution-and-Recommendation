import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, 'data')
SRC_PATH = os.path.join(BASE_PATH, 'src')
TABLES_PATH = os.path.join(DATA_PATH, 'tables')