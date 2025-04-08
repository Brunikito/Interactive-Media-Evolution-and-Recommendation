import pandas as pd
import numpy as np
import os
from random_username.generate import generate_username
from multiprocessing import Pool
from src.generators.cython.cy_user_generator import (
    get_sleep_time_vectorized, get_wake_up_time_vectorized, init_data
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
# 3. Optimize DataFrame memory usage
##############################################################################
# Optimize data types to reduce storage size
def optimize_df_users(df):
    df['user_id'] = df['user_id'].astype('int32')
    df['user_name'] = df['user_name'].astype('category')
    df['user_bed_time'] = df['user_bed_time'].astype('float32')
    df['user_wake_time'] = df['user_wake_time'].astype('float32')
    df['user_lunch_time'] = df['user_lunch_time'].astype('float32')
    df['user_dinner_time'] = df['user_dinner_time'].astype('float32')
    df['user_work_time'] = df['user_work_time'].astype('int8')
    df['user_free_from_work_time'] = df['user_free_from_work_time'].astype('int8')
    df['user_work_days'] = df['user_work_days'].astype('int8')
    df['user_age'] = df['user_age'].astype('int8')
    df['user_gender'] = df['user_gender'].astype('category')
    df['user_location'] = df['user_location'].astype('category')
    df['user_language'] = df['user_language'].astype('category')
    df['user_ocupation'] = df['user_ocupation'].astype('category')
    df['user_education'] = df['user_education'].astype('int8')
    df['user_video_watching_time'] = df['user_video_watching_time'].astype('float32')
    df['user_video_retention_time'] = df['user_video_retention_time'].astype('float32')
    return df

def optimize_df_USER(df):
    df['UserID'] = df['UserID'].astype('int32')
    df['UserName'] = df['UserName'].astype('category')
    df['UserEmail'] = df['UserEmail'].astype('category')
    df['UserPassword'] = df['UserPassword'].astype('category')
    df['UserPhoto'] = df['UserPhoto'].astype('category')
    return df

##############################################################################
# 4. Main user generation function
##############################################################################

def create_random_user(number_of_users, start_id):
    rng = np.random.default_rng()
    
    user_id = np.arange(start_id, start_id + number_of_users)
    user_name = generate_username(number_of_users)
    user_age = np.clip(rng.negative_binomial(5, 0.15, number_of_users), 4, 100).astype(np.int32)
    user_gender = rng.choice(['M', 'F'], size=number_of_users)
    user_location = rng.choice(country_data['ISO3'].unique(), size=number_of_users, p=probabilities_country)

    # Assign occupation based on age
    user_ocupation = np.empty(number_of_users, dtype=object)
    user_ocupation[user_age < 6] = 'Estudante pré-escola'
    user_ocupation[(user_age >= 6) & (user_age < 11)] = 'Estudante ensino fundamental I'
    user_ocupation[(user_age >= 11) & (user_age < 15)] = 'Estudante ensino fundamental II'
    user_ocupation[(user_age >= 15) & (user_age < 18)] = 'Estudante ensino médio'
    user_ocupation[(user_age >= 18) & (user_age < 23)] = 'Estudante universitário'
    mask_work = user_age >= 23
    user_ocupation[mask_work] = rng.choice(work_data_jobs['ocupation'].values, size=mask_work.sum())

    # Map occupation attributes via dicts
    user_work_time = np.array([occupation_to_work_time.get(occ, 8) for occ in user_ocupation])
    user_free_from_work_time = np.array([occupation_to_free_time.get(occ, 17) for occ in user_ocupation])
    user_work_days = np.array([occupation_to_days_work.get(occ, 5) for occ in user_ocupation])

    # Sleep and wake times
    user_sleep_duration = get_sleep_time_vectorized(user_location, user_age, rng=rng)
    user_wake_time = get_wake_up_time_vectorized(user_work_time, rng=rng)
    user_bed_time = user_work_time - user_sleep_duration

    # Lunch and dinner times
    user_lunch_time = generate_eat_time_vectorized(mean=np.full(number_of_users, 12), minimum=np.full(number_of_users, 11), maximum=np.full(number_of_users, 14), rng=rng)
    dinner_min = np.minimum(17, 24 + user_bed_time - 2)
    dinner_max = np.minimum(23, 24 + user_bed_time - 0.5)
    dinner_mean = np.minimum(20, 24 + user_bed_time - 1)
    user_dinner_time = generate_eat_time_vectorized(mean=dinner_mean, minimum=dinner_min, maximum=dinner_max, alpha=3, rng=rng)

    # Language assignment
    def choose_languages_fast(iso3):
        langs = iso3_to_languages.get(iso3, ['EN'])
        if len(langs) > 1:
            extra = rng.choice(langs[1:], size=rng.integers(0, len(langs)), replace=False)
            return ','.join([langs[0]] + list(extra))
        return langs[0]
    
    user_language = np.array([choose_languages_fast(iso) for iso in user_location])

    # Education level estimation
    user_education = np.where(user_age < 6,
                              0,
                              np.where(user_age < 23, user_age - 6, rng.binomial(16, 0.75, size=number_of_users)))

    # Other attributes
    user_video_watching_time = rng.beta(2, 4, number_of_users) * 6
    user_video_retention_time = rng.beta(2, 4, number_of_users)
    user_timezone = np.array([iso3_to_timezone.get(loc, 0) for loc in user_location])

    # Time adjustment to local timezones
    adjust_time = lambda time: (time + user_timezone) % 24

    df_new_users = pd.DataFrame({
        'user_id': user_id,
        'user_name': user_name,
        'user_bed_time': adjust_time(user_bed_time),
        'user_wake_time': adjust_time(user_wake_time),
        'user_lunch_time': adjust_time(user_lunch_time),
        'user_dinner_time': adjust_time(user_dinner_time),
        'user_work_time': adjust_time(user_work_time),
        'user_free_from_work_time': adjust_time(user_free_from_work_time),
        'user_work_days': user_work_days,
        'user_age': user_age,
        'user_gender': user_gender,
        'user_location': user_location,
        'user_language': user_language,
        'user_ocupation': user_ocupation,
        'user_education': user_education,
        'user_video_watching_time': user_video_watching_time,
        'user_video_retention_time': user_video_retention_time,
        'user_channel_id': None,
        'user_admin_channel_id': None,
    })

    df_new_USER = pd.DataFrame({
        'UserID': user_id,
        'UserName': user_name,
        'UserEmail': [f"{name}{uid}@gmail.com" for name, uid in zip(user_name, user_id)],
        'UserPassword': [''.join(rng.choice(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'), 10))
                         for _ in user_id],
        'UserPhoto': [f"mimi.com/images/user={name}{uid}" for name, uid in zip(user_name, user_id)]
    })

    return optimize_df_users(df_new_users), optimize_df_USER(df_new_USER)
