import pandas as pd
import numpy as np
import datetime

import recommendate
import table_operations
import initialize

# load the tables
channels = pd.read_csv('../data/channels.csv')
comments = pd.read_csv('../data/comments.csv')
content = pd.read_csv('../data/content.csv')
users = pd.read_csv('../data/users.csv')
country_data = pd.read_csv('../data/behavior_generated/country_data_cleaned.csv')
sleep_data = pd.read_csv('../data/behavior_generated/sleep_hours_by_age_country.csv')
work_data = pd.read_csv('../data/behavior_generated/work_behavior.csv')

'''
def create_random_user(number_of_users):
    'user_id', #
    'user_name', #
    'user_bed_time', #
    'user_wake_time', #
    'user_lunch_time', #
    'user_dinner_time', #
    'user_exercise_time', #
    'user_work_time', #
    'user_free_from_work_time', #
    'user_work_days', #
    'user_age', #
    'user_gender', #
    'user_location', #
    'user_language', #
    'user_ocupation', #
    'user_education', #
    'user_video_watching_time', #
    'user_video_retention_time', #'''