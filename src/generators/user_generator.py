import pandas as pd
import numpy as np
import os
from src.generators.cython.cy_user_generator import (
    get_sleep_time_vectorized, get_wake_up_time_vectorized, init_data,
    generate_user_languages
)

# Get current directory (adjust if needed)
actual_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Load data files
init_data()

# Load CSV data
channels = pd.read_csv(os.path.join(actual_dir, 'data/channels.csv'))
comments = pd.read_csv(os.path.join(actual_dir, 'data/comments.csv'))
content = pd.read_csv(os.path.join(actual_dir, 'data/content.csv'))
users = pd.read_csv(os.path.join(actual_dir, 'data/users.csv'))
country_data = pd.read_csv(os.path.join(actual_dir, 'data/behavior_generated/country_data_cleaned.csv'))
sleep_data = pd.read_csv(os.path.join(actual_dir, 'data/behavior_generated/sleep_hours_by_age_country.csv'))
work_data = pd.read_csv(os.path.join(actual_dir, 'data/behavior_generated/work_behavior.csv'))

# Pre-calculate population fractions for sampling
total_population = country_data['Population'].sum()
country_data['Population_Fraction'] = country_data['Population'] / total_population
probabilities_country = country_data['Population_Fraction'].values

# Filter out student occupations from work_data
work_data_jobs = work_data[~work_data['ocupation'].isin([
    'Estudante pré-escola', 'Estudante ensino fundamental I', 
    'Estudante ensino fundamental II', 'Estudante ensino médio', 
    'Estudante universitário'
])]


##############################################################################
# 2. Build dictionaries for occupation mappings and language lookups
##############################################################################

# Convert time strings into integer hours
work_data['work_time_hour'] = work_data['work_time'].str.split(':').str[0].astype(int)
work_data['free_time_hour'] = work_data['free_from_work_time'].str.split(':').str[0].astype(int)

# Build dictionaries for mapping occupations
occupation_to_work_time = work_data.set_index('ocupation')['work_time_hour'].to_dict()
occupation_to_free_time = work_data.set_index('ocupation')['free_time_hour'].to_dict()
occupation_to_days_work = work_data.set_index('ocupation')['days_work'].to_dict()

# Build language dictionary from ISO3
iso3_to_languages = {
    row['ISO3']: row['Languages'].split(',') 
    for _, row in country_data.iterrows()
}

iso3_to_first_language = {
    row['ISO3']: row['Languages'].split(',')[0] 
    for _, row in country_data.iterrows()
}

all_languages = np.unique(
    [lang for langs in iso3_to_languages.values() for lang in langs]
    )

# Suporte: arrays alinhados para ISO3 -> linguagem
iso3_keys = np.array(sorted(iso3_to_first_language.keys()))
iso3_firstlangs = np.array([iso3_to_first_language[k] for k in iso3_keys], dtype=object)

def get_primary_languages(user_location, iso3_keys, iso3_firstlangs):
    # Vetoriza o mapeamento de ISO3 -> idioma primário
    indices = np.searchsorted(iso3_keys, user_location)
    return iso3_firstlangs[indices]

def choose_languages_fast(iso3, rng):
    firstlang = iso3_to_first_language.get(iso3, ['en'])
    extra_langs = rng.choice(all_languages, 2, replace=True)
    return ','.join(set([firstlang] + extra_langs.tolist()))

# Timezone dictionary
iso3_to_timezone = dict(zip(country_data['ISO3'], country_data['Timezone']))

def generate_eat_time_vectorized(mean, minimum, maximum, alpha=2, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    normalized_mean = (mean - minimum) / (maximum - minimum)
    beta_param = alpha * (1 - normalized_mean) / normalized_mean
    beta_values = rng.beta(alpha, beta_param)
    return minimum + (maximum - minimum) * beta_values

##############################################################################
# 4. Main user generation function
##############################################################################

import time

def create_random_user(number_of_users, start_id):
    rng = np.random.default_rng()
    
    user_id = np.arange(start_id, start_id + number_of_users).astype(np.int32)
    user_name = rng.integers(0, 1000, size=number_of_users).astype(np.int16)
    
    user_age = np.clip(rng.negative_binomial(5, 0.15, number_of_users), 4, 100).astype(np.int32)
    user_gender = rng.choice(['M', 'F'], size=number_of_users)
    user_location = rng.choice(country_data['ISO3'].unique(), size=number_of_users, p=probabilities_country)
    
    user_ocupation = np.empty(number_of_users, dtype=object)
    user_ocupation[user_age < 6] = 'Estudante pré-escola'
    user_ocupation[(user_age >= 6) & (user_age < 11)] = 'Estudante ensino fundamental I'
    user_ocupation[(user_age >= 11) & (user_age < 15)] = 'Estudante ensino fundamental II'
    user_ocupation[(user_age >= 15) & (user_age < 18)] = 'Estudante ensino médio'
    user_ocupation[(user_age >= 18) & (user_age < 23)] = 'Estudante universitário'
    mask_work = user_age >= 23
    user_ocupation[mask_work] = rng.choice(work_data_jobs['ocupation'].values, size=mask_work.sum())
    
    user_work_time = np.array([occupation_to_work_time.get(occ, 8) for occ in user_ocupation])
    user_free_from_work_time = np.array([occupation_to_free_time.get(occ, 17) for occ in user_ocupation])
    user_work_days = np.array([occupation_to_days_work.get(occ, 5) for occ in user_ocupation])
    
    user_sleep_duration = get_sleep_time_vectorized(user_location, user_age, rng=rng)
    user_wake_time = get_wake_up_time_vectorized(user_work_time, rng=rng)
    user_bed_time = user_work_time - user_sleep_duration
    
    user_lunch_time = generate_eat_time_vectorized(
        mean=np.full(number_of_users, 12),
        minimum=np.full(number_of_users, 11),
        maximum=np.full(number_of_users, 14),
        rng=rng
    )

    dinner_min = np.minimum(17, 24 + user_bed_time - 2)
    dinner_max = np.minimum(23, 24 + user_bed_time - 0.5)
    dinner_mean = np.minimum(20, 24 + user_bed_time - 1)

    user_dinner_time = generate_eat_time_vectorized(
        mean=dinner_mean,
        minimum=dinner_min,
        maximum=dinner_max,
        alpha=3,
        rng=rng
    )
    
    primary_languages = get_primary_languages(user_location, iso3_keys, iso3_firstlangs).astype(np.object_)
    extra_langs = rng.choice(all_languages, size=(len(user_location), 2), replace=True).astype(np.object_)
    user_language = generate_user_languages(primary_languages, extra_langs)
    
    user_education = np.where(user_age < 6,
                              0,
                              np.where(user_age < 23, user_age - 6, rng.binomial(16, 0.75, size=number_of_users)))
    
    user_video_watching_time = rng.beta(2, 4, number_of_users) * 6
    user_video_retention_time = rng.beta(2, 4, number_of_users)
    user_timezone = np.array([iso3_to_timezone.get(loc, 0) for loc in user_location])
    
    adjust_time = lambda time: (time + user_timezone) % 24

    zeros = np.zeros(number_of_users, dtype=bool)
    df_new_users = pd.DataFrame({
        'user_id': user_id,
        'user_name': pd.Categorical(user_name),
        'user_bed_time': adjust_time(user_bed_time).astype(np.float16),
        'user_wake_time': adjust_time(user_wake_time).astype(np.float16),
        'user_lunch_time': adjust_time(user_lunch_time).astype(np.float16),
        'user_dinner_time': adjust_time(user_dinner_time).astype(np.float16),
        'user_work_time': adjust_time(user_work_time).astype(np.int8),
        'user_free_from_work_time': adjust_time(user_free_from_work_time).astype(np.int8),
        'user_work_days': user_work_days.astype(np.int8),
        'user_age': user_age.astype(np.int8),
        'user_gender': pd.Categorical(user_gender),
        'user_location': pd.Categorical(user_location),
        'user_language': pd.Categorical(user_language),
        'user_ocupation': pd.Categorical(user_ocupation),
        'user_education': user_education.astype(np.int8),
        'user_video_watching_time': user_video_watching_time.astype(np.float16),
        'user_video_retention_time': user_video_retention_time.astype(np.float16),
        'user_channel_id': zeros,
        'user_admin_channel_id': zeros,
    })
    
    ones = np.ones(number_of_users, dtype=bool)
    df_new_USER = pd.DataFrame({
        'UserID': user_id,
        'UserName': pd.Categorical(user_name),
        'UserEmail': ones,
        'UserPassword': ones,
        'UserPhoto': ones,
    })

    return df_new_users, df_new_USER