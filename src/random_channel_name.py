import numpy as np
import os
from numba import njit
from typing import List

# === Pré-carregamento de arquivos ===
actual_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(actual_dir, '../data/words/adjectives.txt'), 'r', encoding='utf-8') as f:
    adjectives = [line.strip().capitalize() for line in f]

with open(os.path.join(actual_dir, '../data/words/nouns.txt'), 'r', encoding='utf-8') as f:
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


# === Pré-processa ===
categories_list = list(category_suffixes.keys())
category_to_index = {k: i for i, k in enumerate(categories_list)}
suffix_array = [np.array([s.capitalize() for s in category_suffixes[k]]) for k in categories_list]

# === Função JIT compilada ===
@njit
def generate_indices(n, n_adjectives, n_nouns, suffixes_lengths, category_indices):
    """
    Gera os índices aleatórios que serão usados para selecionar adjetivos, substantivos e sufixos.
    """
    adjective_ids = np.random.randint(0, n_adjectives, size=n)
    noun_ids = np.random.randint(0, n_nouns, size=n)
    suffix_ids = np.empty(n, dtype=np.int32)

    for i in range(n):
        suffix_len = suffixes_lengths[category_indices[i]]
        suffix_ids[i] = np.random.randint(0, suffix_len)

    return adjective_ids, noun_ids, suffix_ids

# === Wrapper Python ===
def generate_channel_name(categories: np.ndarray) -> np.ndarray:
    n = len(categories)

    # Converte strings para NumPy arrays e prepara os dados
    adjectives_np = np.array(adjectives)
    nouns_np = np.array(nouns)
    category_indices = np.array([category_to_index[c] for c in categories])
    suffixes_lengths = np.array([len(suffix_array[i]) for i in range(len(suffix_array))])

    # Gera índices de forma JIT
    adj_ids, noun_ids, suffix_ids = generate_indices(
        n, len(adjectives), len(nouns), suffixes_lengths, category_indices
    )

    # Monta os nomes com capitalização fora do Numba
    return np.array([
        adjectives_np[adj] + ' ' + nouns_np[noun] + ' ' + suffix_array[cat][suff]
        for adj, noun, cat, suff in zip(adj_ids, noun_ids, category_indices, suffix_ids)
    ])

# === Execução ===
if __name__ == '__main__':
    import timeit

    n = 1_000_000
    categories_np = np.array(list(category_suffixes.keys()))
    random_categories = np.random.choice(categories_np, size=n)

    t0 = timeit.default_timer()
    channel_names = generate_channel_name(random_categories)
    t1 = timeit.default_timer()

    print(f"Tempo de execução para gerar nomes de canais: {t1 - t0:.4f} segundos")
    print(channel_names[:10])