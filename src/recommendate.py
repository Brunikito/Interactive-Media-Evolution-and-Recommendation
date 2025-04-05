import pandas as pd

def recommendate(path_tables, num_recomendations: int = 10) -> pd.DataFrame:
    """
    Recommend content to users based on their watch history and popular content.
    This function loads the necessary tables, processes the data, and returns a DataFrame with recommendations.
    """
    # Load the necessary tables
    user = pd.read_csv(f'{path_tables}/USER.csv')
    uwatchingcont = pd.read_csv(f'{path_tables}/UWATCHINGCONT.csv')
    content_conttag = pd.read_csv(f'{path_tables}/CONTENT_CONTTag.csv')

    # Prepare recommendations for each user
    recommendations = []

    # Get unique users
    unique_users = uwatchingcont['UserID'].unique()

    for user_id in user['UserID']:
        if user_id in unique_users:
            # Filter the last 5 watched content for the current user
            user_watches = uwatchingcont[uwatchingcont['UserID'] == user_id]
            user_watches = user_watches.sort_values(by='UWatchCONTDateTime', ascending=False).head(8)

            # Extract tags from the last watched content
            tags = content_conttag[content_conttag['ContentID'].isin(user_watches['ContentID'])]
            
            if tags.empty:  # If no tags available, use a default strategy
                top_tags = []
            else:
                top_tags = tags['CONTTag'].value_counts().head(5).index.tolist()

            if top_tags:  # If there are any tags, use them to filter recommended content
                tagged_content = content_conttag[content_conttag['CONTTag'].isin(top_tags)]
            else:
                tagged_content = content_conttag  # If no tags, recommend any content

            # Calculate popular content
            popular_content = uwatchingcont.groupby('ContentID').size().reset_index(name='WatchCount')
            popular_content = popular_content.sort_values(by='WatchCount', ascending=False)

            # Get recommended content IDs based on tags and popularity
            recommended_content_ids = popular_content[popular_content['ContentID'].isin(tagged_content['ContentID'])]
            recommended_content_ids = recommended_content_ids.head(num_recomendations)['ContentID'].tolist()

            # Ensure the user doesn't get already watched content
            recommended_content_ids = [content_id for content_id in recommended_content_ids if content_id not in user_watches['ContentID'].values]
            
            # If not enough recommendations, fill with additional popular content
            if len(recommended_content_ids) < num_recomendations:
                additional_content = popular_content[~popular_content['ContentID'].isin(recommended_content_ids)]
                additional_content = additional_content.head(num_recomendations - len(recommended_content_ids))['ContentID'].tolist()
                recommended_content_ids.extend(additional_content)
            
        else:
            # Recommend the most popular content for users with no watch history
            popular_content = uwatchingcont.groupby('ContentID').size().reset_index(name='WatchCount')
            popular_content = popular_content.sort_values(by='WatchCount', ascending=False)
            recommended_content_ids = popular_content.head(num_recomendations)['ContentID'].tolist()

        # Append recommendations for the current user
        recommendations.append({'UserID': user_id, 'Recommendations': recommended_content_ids})

    # Convert recommendations to a DataFrame
    recommendations_df = pd.DataFrame(recommendations)

    return recommendations_df
