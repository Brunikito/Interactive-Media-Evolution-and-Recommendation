import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.dirname(current_dir)

sys.path.append(src)

from generators.user_generator import create_random_user  # ou o path correto

def process_batch(args):
    batch_size, start_id = args
    return create_random_user(batch_size, start_id)