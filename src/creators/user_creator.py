from src.generators.user_generator import create_random_user

if __name__ == '__main__':
    import pyarrow as pa
    import pyarrow.parquet as pq
    
    import pandas as pd
    from multiprocessing import Pool
    import os
    from src import DATA_PATH, BASE_PATH
    
    users = pd.read_csv(os.path.join(DATA_PATH, 'users.csv'))

    print('Creating random users...')
    
    number_of_users = 1_000_000
    import timeit
    start_time = timeit.default_timer()
    df_new_users, df_new_USER = create_random_user(number_of_users, users.shape[0])
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print('Users created.')
    print(f'Elapsed time: {elapsed_time:.2f} seconds')
    print('Memory Usage:')
    print('df_new_users:', df_new_users.memory_usage().sum() / (1024 ** 2), 'MB')
    print('df_new_USER:', df_new_USER.memory_usage().sum() / (1024 ** 2), 'MB')
    print('Saving users...')
    df_new_users.to_parquet(os.path.join(BASE_PATH, 'usuarios_full.parquet'), index=False, engine='pyarrow', compression='snappy')
    df_new_USER.to_parquet(os.path.join(BASE_PATH, 'USERS.parquet'), index=False, engine='pyarrow', compression='snappy')
    print('Users saved.')
    '''with open("timing_log_users.txt", "w") as f:
        f.write("Etapas de tempo para create_random_content:\n\n")
        for step, duration in timings.items():
            f.write(f"{step}: {duration:.6f} segundos\n")'''
    
    