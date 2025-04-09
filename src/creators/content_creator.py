from src import BASE_PATH
from src.generators.content_generator import create_random_content, CATEGORIES
import pandas as pd
import os
import time

if __name__ == '__main__':
    channels = pd.read_parquet(os.path.join(BASE_PATH, 'channels_full.parquet'))
    print('creating content...')
    start = time.perf_counter()
    result = create_random_content(channels, CATEGORIES, 1, 0, '2025-04-08')
    end = time.perf_counter()
    print('done')
    print('Time taken:', end - start)
    print("#"*50)

    def print_memory_usage(name, df):
        mem_mb = df.memory_usage(deep=True).sum() / 1024**2
        print(f"{name}: {mem_mb:.2f} MB")

    for name, df in result.items():
        if isinstance(df, pd.DataFrame):
            print_memory_usage(name, df)

    print("#"*50)
    mem_info = result['df_content'].memory_usage(deep=True).sort_values(ascending=False)
    print(mem_info / 1024**2)

    # Logs
    with open("timing_log.txt", "w") as f:
        f.write("Etapas de tempo para create_random_content:\n\n")
        for step, duration in result["timings"].items():
            f.write(f"{step}: {duration:.6f} segundos\n")
    