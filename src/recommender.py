"""Content-based music recommender: load songs, score them against a user's taste, and rank."""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Scoring weights (the "Algorithm Recipe" from Phase 2).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5
ACOUSTIC_THRESHOLD = 0.5  # acousticness >= this counts as an "acoustic" song

# Columns in songs.csv that must be treated as numbers, not text.
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")


@dataclass
class Song:
    """A single song and its audio/metadata attributes."""
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
    """A user's taste preferences used to score songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    fav_genre: str,
    fav_mood: str,
    target_energy: float,
    likes_acoustic,
) -> Tuple[float, List[str]]:
    """Shared scoring core: return a numeric score and a list of human-readable reasons."""
    score = 0.0
    reasons: List[str] = []

    if fav_genre is not None and genre == fav_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({genre}) +{GENRE_WEIGHT:.1f}")

    if fav_mood is not None and mood == fav_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({mood}) +{MOOD_WEIGHT:.1f}")

    if target_energy is not None:
        # Reward closeness to the target, not just high energy.
        points = ENERGY_WEIGHT * (1.0 - abs(energy - target_energy))
        points = max(0.0, points)
        score += points
        reasons.append(f"energy close to {target_energy:.2f} +{points:.2f}")

    if likes_acoustic is not None:
        is_acoustic = acousticness >= ACOUSTIC_THRESHOLD
        if is_acoustic == bool(likes_acoustic):
            score += ACOUSTIC_WEIGHT
            feel = "acoustic" if likes_acoustic else "non-acoustic"
            reasons.append(f"{feel} feel +{ACOUSTIC_WEIGHT:.1f}")

    return score, reasons


class Recommender:
    """Ranks a catalog of Song objects against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score one Song against a UserProfile."""
        return _score(
            song.genre, song.mood, song.energy, song.acousticness,
            user.favorite_genre, user.favorite_mood, user.target_energy, user.likes_acoustic,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs sorted from best to worst match for the user."""
        ranked = sorted(self.songs, key=lambda s: self._score_song(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song fits the user."""
        score, reasons = self._score_song(user, song)
        if not reasons:
            return f"General pick (score {score:.2f}); no strong feature matches."
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV into a list of dicts, converting numeric fields to numbers."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in FLOAT_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song dict against a user_prefs dict; return (score, reasons)."""
    return _score(
        song["genre"], song["mood"], song["energy"], song["acousticness"],
        user_prefs.get("genre"), user_prefs.get("mood"),
        user_prefs.get("energy"), user_prefs.get("likes_acoustic"),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong feature matches"
        scored.append((song, score, explanation))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
