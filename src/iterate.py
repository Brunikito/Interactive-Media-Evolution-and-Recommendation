import pandas as pd
import numpy as np
import datetime

import recommendate
import table_operations
import os

# load the tables
channels = pd.read_csv('data/channels.csv')
comments = pd.read_csv('data/comments.csv')
content = pd.read_csv('data/content.csv')
users = pd.read_csv('data/users.csv')

