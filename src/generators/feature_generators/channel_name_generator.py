# main.py
import numpy as np
import os
from .cython.namegen import generate_indices
from src import DATA_PATH
# === Pré-carregamento ===

words_dir = os.path.join(DATA_PATH, 'words')

with open(os.path.join(words_dir, 'adjectives.txt'), 'r', encoding='utf-8') as f:
    adjectives = [line.strip().capitalize() for line in f]

with open(os.path.join(words_dir, 'nouns.txt'), 'r', encoding='utf-8') as f:
    nouns = [line.strip().capitalize() for line in f]

category_suffixes = {
    "Animals": [
        "garden", "world", "zone", "realm", "kingdom", "safari", "tales", "wild", 
        "adventure", "explore", "nature", "life", "tribe", "beast", "den", "paws"
    ],
    "Automobiles": [
        "drive", "speed", "garage", "road", "auto", "gear", "shift", "track", "riders", 
        "zone", "race", "car", "wheel", "machine", "pit", "motors"
    ],
    "Science & Technology": [
        "lab", "hub", "zone", "world", "tech", "sphere", "network", "innovations", "future", 
        "cyber", "digital", "engine", "logic", "machine", "research", "solutions"
    ],
    "Comedy": [
        "show", "world", "times", "laughs", "club", "laugh", "fun", "jokes", "skits", 
        "humor", "giggle", "comedy", "standup", "zone", "sitcom", "sketch"
    ],
    "Education": [
        "hub", "zone", "world", "class", "study", "academy", "school", "learning", 
        "lessons", "institute", "guide", "curriculum", "mastery", "campus", "course", "tutorial"
    ],
    "Entertainment": [
        "world", "show", "stream", "cast", "zone", "media", "hub", "broadcast", 
        "network", "performance", "theater", "stage", "live", "scene", "crew", "stars"
    ],
    "Sports": [
        "league", "zone", "world", "arena", "club", "play", "game", "team", "match", 
        "training", "championship", "court", "field", "competition", "stadium", "pro"
    ],
    "Film & Animation": [
        "studio", "world", "cast", "cinema", "realm", "scene", "animation", "film", 
        "production", "theater", "director", "movie", "story", "crew", "edit", "vision"
    ],
    "How-to & Style": [
        "guide", "world", "style", "zone", "academy", "tutorial", "fashion", "tips", 
        "advice", "inspiration", "howto", "masterclass", "solutions", "insight", "method", "trend"
    ],
    "Gaming": [
        "hub", "zone", "world", "games", "arena", "play", "quest", "challenge", "level", 
        "gamer", "battle", "league", "arcade", "realm", "pro", "strategy"
    ],
    "Music": [
        "studio", "sound", "world", "zone", "vibes", "track", "beat", "melody", "rhythm", 
        "tune", "band", "notes", "song", "album", "wave", "soundscape"
    ],
    "News & Politics": [
        "news", "hub", "daily", "times", "report", "press", "watch", "coverage", 
        "updates", "broadcast", "insight", "politics", "analysis", "story", "coverage", "headlines"
    ],
    "People & Blogs": [
        "journal", "world", "life", "blog", "diary", "stories", "adventures", "experience", 
        "diaries", "daily", "vlog", "thoughts", "expressions", "voice", "memories", "insights"
    ],
    "Nonprofits & Activism": [
        "cause", "world", "action", "impact", "movement", "network", "change", "voice", 
        "project", "campaign", "effort", "solutions", "activism", "mission", "purpose", "unity"
    ],
    "Travel & Events": [
        "journey", "tour", "world", "events", "explore", "adventure", "globe", "escape", 
        "vacation", "trip", "voyage", "path", "discoveries", "trek", "experience", "tourism"
    ]
}

categories_list = list(category_suffixes.keys())
category_to_index = {k: i for i, k in enumerate(categories_list)}
suffix_array = [np.array([s.capitalize() for s in category_suffixes[k]]) for k in categories_list]

def generate_channel_name(categories: np.ndarray) -> np.ndarray:
    n = len(categories)
    adjectives_np = np.array(adjectives)
    nouns_np = np.array(nouns)

    category_indices = np.array([category_to_index[c] for c in categories], dtype=np.int32)
    suffixes_lengths = np.array([len(sa) for sa in suffix_array], dtype=np.int32)

    adj_ids, noun_ids, suffix_ids = generate_indices(
        n, len(adjectives), len(nouns), suffixes_lengths, category_indices
    )

    return np.array([
        f"{adjectives_np[adj]} {nouns_np[noun]} {suffix_array[cat][suff]}"
        for adj, noun, cat, suff in zip(adj_ids, noun_ids, category_indices, suffix_ids)
    ])


# === Função auxiliar para gerar nomes em batch ===
def generate_batch(batch_categories):
    return generate_channel_name(np.array(batch_categories))

# Execução
if __name__ == '__main__':
    import timeit    
    from multiprocessing import Pool, cpu_count


    n = 1_000_000
    batch_size = 10_000  # Ajuste conforme sua RAM
    categories_np = np.array(list(category_suffixes.keys()))
    random_categories = np.random.choice(categories_np, size=n)

    # Quebrar em batches
    batches = [random_categories[i:i + batch_size] for i in range(0, n, batch_size)]

    t0 = timeit.default_timer()

    with Pool(cpu_count()) as pool:
        results = pool.map(generate_batch, batches)

    # Concatenar os resultados
    names = np.concatenate(results)

    t1 = timeit.default_timer()

    print(f"Tempo de execução: {t1 - t0:.4f}s")
    print(names[:10])