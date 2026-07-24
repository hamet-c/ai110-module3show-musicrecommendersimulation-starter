"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# Profiles we test the recommender against.
# The first three are normal "personas"; the last two are adversarial
# edge cases with conflicting or catalog-missing preferences.
PROFILES = {
    "High-Energy Pop":   {"genre": "pop",     "mood": "happy",   "energy": 0.9},
    "Chill Lofi":        {"genre": "lofi",    "mood": "chill",   "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock",    "mood": "intense", "energy": 0.9},
    # Adversarial: high energy but a sad mood (should not coexist in real music).
    "Conflicting (loud + sad)": {"genre": "pop", "mood": "sad", "energy": 0.95},
    # Adversarial: a genre/mood combo that appears in ZERO catalog songs.
    "Impossible (metal + relaxed)": {"genre": "metal", "mood": "relaxed", "energy": 0.5},
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print one profile's top picks in a clean terminal layout."""
    print()
    print("=" * 52)
    print(f"  {name}")
    print(f"  genre={user_prefs['genre']}  mood={user_prefs['mood']}  energy={user_prefs['energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  {rank}. {song['title']} - {song['artist']}")
        print(f"     score: {score:.2f}")
        print(f"     why:   {explanation}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
