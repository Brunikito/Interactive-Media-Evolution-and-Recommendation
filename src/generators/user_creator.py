##############################################################################
# 5. Parallel execution to generate large user base
##############################################################################

from src.utils.processing_ucreation import process_batch
from .user_generator import create_random_user

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
    
    '''number_of_users = 1_000_000
    batch_size = 10000
    initial_id = users.shape[0]
    import timeit
    start_time = timeit.default_timer()
    # Prepare batches with correct ID ranges
    batches = [(min(batch_size, number_of_users - i), initial_id + i)
                for i in range(0, number_of_users, batch_size)]

    users_path = 'usuarios_full.parquet'
    user_table_path = 'USERS.parquet'

    # Gerar o primeiro batch só pra pegar o schema
    first_df_users, first_df_USER = create_random_user(*batches[0])
    schema_users = pa.Schema.from_pandas(first_df_users)
    schema_USER = pa.Schema.from_pandas(first_df_USER)

    with pq.ParquetWriter(users_path, schema=schema_users, use_dictionary=True, compression='snappy') as user_writer, \
        pq.ParquetWriter(user_table_path, schema=schema_USER, use_dictionary=True, compression='snappy') as user_table_writer:

        with Pool() as pool:
            for result in pool.imap_unordered(process_batch, batches, chunksize=4):
                df_users, df_USER = result

                table_users = pa.Table.from_pandas(df_users, schema=schema_users)
                table_USER = pa.Table.from_pandas(df_USER, schema=schema_USER)

                user_writer.write_table(table_users)
                user_table_writer.write_table(table_USER)


    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time
    print('Users created and saved.')
    print(f'Elapsed time: {elapsed_time:.2f} seconds')

    df_users = pd.read_parquet(users_path)
    df_USER = pd.read_parquet(user_table_path)
    print('Memory Usage:')
    print(df_users.memory_usage().sum() / (1024 ** 2), 'MB')
    print(df_USER.memory_usage().sum() / (1024 ** 2), 'MB')'''