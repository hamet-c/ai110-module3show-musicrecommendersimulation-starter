import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read the CSV into a list of song dicts, converting numeric columns to int/float."""
    int_fields = ("id", "tempo_bpm")
    float_fields = ("energy", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs

# Scoring weights. Adjust these to run experiments.
# Default recipe: genre 2.0, mood 1.0, energy up to 1.0, acoustic 0.5.
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Genre match: strongest signal.
    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"matches your favorite genre ({song['genre']})")

    # Mood match: worth half of a genre match.
    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"matches your mood ({song['mood']})")

    # Energy closeness: continuous tie-breaker, up to ENERGY_WEIGHT for an exact match.
    if "energy" in user_prefs:
        closeness = (1.0 - abs(user_prefs["energy"] - song["energy"])) * ENERGY_WEIGHT
        score += closeness
        if closeness > 0.8 * ENERGY_WEIGHT:
            reasons.append("very close to your energy level")

    # Acoustic preference: small nudge, only if the profile states one.
    if "likes_acoustic" in user_prefs:
        song_is_acoustic = song["acousticness"] > 0.5
        if song_is_acoustic == user_prefs["likes_acoustic"]:
            score += ACOUSTIC_WEIGHT
            reasons.append("matches your acoustic preference")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k as (song, score, explanation) tuples."""
    # Score every song. Each entry carries the song, its score, and reasons.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # Rank: sort a new list by score, highest first, and keep the top k.
    ranked = sorted(scored, key=lambda entry: entry[1], reverse=True)
    return ranked[:k]
