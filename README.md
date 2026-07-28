# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real-world recommenders work

Big platforms like Spotify, YouTube, and TikTok mostly blend two strategies:

- **Collaborative filtering** — "people like *you* also liked this." It ignores what a
  song sounds like and instead learns from the behavior of many users (likes, skips,
  replays, playlist adds). If lots of people with taste similar to mine liked a song,
  it recommends that song to me. It's powerful but needs a large crowd of users and lots
  of interaction history, so it struggles with brand-new users or songs (the "cold-start"
  problem).
- **Content-based filtering** — "this song is *similar to* what you already like." It
  ignores other users and compares the *attributes* of songs (genre, mood, energy, tempo)
  to a user's preferences. It works even for a single user with no crowd data.

**My version is a content-based recommender.** With only 10 songs and one user profile, I
have no crowd behavior to learn from, so I compare each song's attributes to a user's taste
profile and rank the closest matches. It prioritizes **genre and mood** as the strongest
signals of taste, and uses **energy** (and optionally acoustic feel) to separate songs that
share a genre but fit a different vibe — for example a high-energy gym track versus a chill
study track.

### Features my objects use

- **`Song`** uses: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`,
  `acousticness` (from `data/songs.csv`).
- **`UserProfile`** stores: `favorite_genre`, `favorite_mood`, `target_energy`, and
  `likes_acoustic`.

The core features that drive scoring are **genre, mood, energy, and acousticness** — a small
set that still captures most of what makes a song "feel" right for a listener.

*(The finalized scoring recipe and expected biases are documented below in Phase 2.)*

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



