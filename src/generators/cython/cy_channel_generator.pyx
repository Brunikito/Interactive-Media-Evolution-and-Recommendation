# cy_channel_generator.pyx
import numpy as np
cimport numpy as cnp
import pandas as pd

# Tipagem estática
ctypedef cnp.int32_t int32_t

# Hard-coded categories
CATEGORIES = np.array([
    'Animals', 'Automobiles', 'Science & Technology', 'Comedy', 'Education',
    'Entertainment', 'Sports', 'Film & Animation', 'How-to & Style', 'Gaming',
    'Music', 'News & Politics', 'People & Blogs', 'Nonprofits & Activism', 'Travel & Events'
], dtype=object)

def create_random_channel(object users_df, float new_channel_ratio, int initial_id, object current_date, object generate_channel_name):
    cdef int num_users = users_df.shape[0]

    # Boolean mask to find users without channel
    mask = users_df["user_channel_id"].isna().to_numpy()
    cdef int available_users = int(mask.sum())
    cdef int num_channels = int(available_users * new_channel_ratio)

    if num_channels == 0:
        return users_df, pd.DataFrame(columns=[
            "channel_id", "channel_name", "channel_creation_date",
            "channel_description", "channel_language", "channel_location",
            "channel_category"
        ])

    # Sample user indices
    idx = np.where(mask)[0]
    selected_idx = np.random.choice(idx, size=num_channels, replace=False)

    # Extract user info
    user_lang = users_df["user_language"].to_numpy()[selected_idx]
    user_loc = users_df["user_location"].to_numpy()[selected_idx]

    # Generate data
    channel_id = np.arange(initial_id, initial_id + num_channels, dtype=np.int32)
    channel_category = np.random.choice(CATEGORIES, size=num_channels)
    channel_name = generate_channel_name(channel_category)
    channel_description = np.full(num_channels, '', dtype=object)
    channel_creation_date = np.full(num_channels, current_date)

    # Update DataFrame
    users_df.loc[selected_idx, "user_channel_id"] = channel_id

    # Build final DataFrame
    channels = pd.DataFrame({
        "channel_id": channel_id,
        "channel_name": channel_name,
        "channel_creation_date": channel_creation_date,
        "channel_description": channel_description,
        "channel_language": user_lang,
        "channel_location": user_loc,
        "channel_category": channel_category
    })

    return users_df, channels
