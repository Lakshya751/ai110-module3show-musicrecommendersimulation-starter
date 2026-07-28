"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog, scores it against a user taste profile, and prints
a ranked, explained list of recommendations.
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(title: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top-k recommendations for one user profile in a readable layout."""
    print("=" * 60)
    print(f"Profile: {title}")
    print(f"Prefs:   {user_prefs}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']} ({song['genre']}/{song['mood']})")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print()


# Diverse user profiles for stress-testing the recommender. The last one is an
# "adversarial" profile with a conflict (high energy but a sad mood) to see whether
# the scoring logic produces something sensible when preferences fight each other.
PROFILES = [
    ("Happy Pop", {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}),
    ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}),
    ("Acoustic Folk", {"genre": "folk", "mood": "sad", "energy": 0.3, "likes_acoustic": True}),
    ("Adversarial: High-Energy Sad", {"genre": "edm", "mood": "sad", "energy": 0.9, "likes_acoustic": False}),
]


def main() -> None:
    songs = load_songs("data/songs.csv")
    print()
    for title, user_prefs in PROFILES:
        print_recommendations(title, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
