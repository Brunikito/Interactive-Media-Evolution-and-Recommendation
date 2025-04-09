# cython: boundscheck=False, wraparound=False, language_level=3
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

import numpy as np
cimport numpy as np
import pandas as pd
import os
from random_username.generate import generate_username
from libc.stdlib cimport rand, srand, malloc, free
from libc.string cimport memcpy, strchr, strlen
from libc.math cimport fmod
from src import DATA_PATH
from cython.parallel import prange

# Typing aliases
ctypedef np.int32_t int32_t
ctypedef np.int8_t int8_t
ctypedef np.float32_t float32_t

np.import_array()

# Tipagem para acelerar
cdef dict sleep_lookup = {}
cdef dict occupation_to_work_time = {}
cdef dict occupation_to_free_time = {}
cdef dict occupation_to_days_work = {}
cdef dict iso3_to_languages = {}
cdef dict iso3_to_timezone = {}
cdef np.ndarray probabilities_country

# DataFrame externos carregados via Python
cdef object country_data
cdef object work_data_jobs

def init_data():
    global country_data, sleep_lookup
    global occupation_to_work_time, occupation_to_free_time, occupation_to_days_work
    global iso3_to_languages, iso3_to_timezone, probabilities_country, work_data_jobs
    global DATA_PATH
    country_data = pd.read_csv(os.path.join(DATA_PATH, 'behavior_generated/country_data_cleaned.csv'))
    sleep_data = pd.read_csv(os.path.join(DATA_PATH, 'behavior_generated/sleep_hours_by_age_country.csv'))
    work_data = pd.read_csv(os.path.join(DATA_PATH, 'behavior_generated/work_behavior.csv'))

    # Probabilidades de país
    probabilities_country = np.asarray(country_data['Population_Fraction'].values, dtype=np.float64)

    # Dicionários
    sleep_lookup = {
        (row['country'], row['age_span']): row['sleep_hours']
        for _, row in sleep_data.iterrows()
    }

    occupation_to_work_time = work_data.set_index('ocupation')['work_time_hour'].to_dict()
    occupation_to_free_time = work_data.set_index('ocupation')['free_from_work_time_hour'].to_dict()
    occupation_to_days_work = work_data.set_index('ocupation')['days_work'].to_dict()

    iso3_to_languages = {
        row['ISO3']: row['Languages'].split(',')
        for _, row in country_data.iterrows()
    }

    iso3_to_timezone = dict(zip(country_data['ISO3'], country_data['Timezone']))

    work_data_jobs = work_data[~work_data['ocupation'].isin([
        'Estudante pré-escola', 'Estudante ensino fundamental I', 
        'Estudante ensino fundamental II', 'Estudante ensino médio', 
        'Estudante universitário'
    ])]

cpdef np.ndarray get_sleep_time_vectorized(np.ndarray user_countries, np.ndarray user_ages,
                                           float minimum=4, float maximum=9, int alpha=6, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    cdef np.ndarray[np.int32_t] age_span = ((user_ages + 9) // 10) * 10
    cdef Py_ssize_t i, n = user_countries.shape[0]
    cdef np.ndarray[np.float64_t] sleep_means = np.empty(n, dtype=np.float64)

    for i in range(n):
        sleep_means[i] = sleep_lookup.get((user_countries[i], age_span[i]), 7)

    normalized_mean = (sleep_means - minimum) / (maximum - minimum)
    beta_param = alpha * (1 - normalized_mean) / normalized_mean
    beta_values = rng.beta(alpha, beta_param)
    return minimum + (maximum - minimum) * beta_values

cpdef np.ndarray get_wake_up_time_vectorized(np.ndarray user_work_time,
                                             float minimum_dif=2, float maximum_dif=0.5, float mean_dif=1,
                                             int alpha=6, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    minimum = user_work_time - minimum_dif
    maximum = user_work_time - maximum_dif
    mean = user_work_time - mean_dif
    normalized_mean = (mean - minimum) / (maximum - minimum)
    beta_param = alpha * (1 - normalized_mean) / normalized_mean
    beta_values = rng.beta(alpha, beta_param)
    return minimum + (maximum - minimum) * beta_values

cpdef generate_user_languages(object[:] prim_langs, object[:, :] extra_langs):
    cdef Py_ssize_t i, n = prim_langs.shape[0]
    cdef list result = []
    cdef object l1, l2, l3

    for i in range(n):
        l1 = prim_langs[i]
        l2 = extra_langs[i, 0]
        l3 = extra_langs[i, 1]

        if l1 == l2 and l1 == l3:
            result.append(l1)
        elif l1 == l2:
            result.append(f"{l1},{l3}")
        elif l1 == l3 or l2 == l3:
            result.append(f"{l1},{l2}")
        else:
            result.append(f"{l1},{l2},{l3}")

    return np.array(result, dtype=str)