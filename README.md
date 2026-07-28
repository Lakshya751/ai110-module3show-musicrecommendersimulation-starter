# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a **CLI-first, content-based recommender**. It loads an 18-song catalog from
CSV, scores every song against a user's taste profile (genre, mood, energy, acoustic feel)
using a weighted rule, and prints a ranked top-k list where each pick comes with the reasons
it was chosen.

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

### The design (Phase 2)

**Dataset.** The catalog was expanded from 10 to **18 songs** so there's real variety to
rank. Added genres include hip-hop, edm, classical, metal, country, r&b, folk, and k-pop, and
added moods include energetic, aggressive, nostalgic, romantic, sad, and dreamy. All songs use
the same headers, and the numeric features stay on a 0.0–1.0 scale (except `tempo_bpm`).

**Example user profile.** A taste profile is a small dictionary of target values:

```python
user_prefs = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,
    "likes_acoustic": False,
}
```

This is specific enough to tell "intense rock" apart from "chill lofi": the genre/mood fields
separate the categories, and the energy target pulls toward high-energy songs while pushing
away from low-energy ones.

**Algorithm Recipe (finalized).** For each song, add up:

| Rule | Points |
|------|--------|
| Genre matches the user's favorite genre | **+2.0** |
| Mood matches the user's favorite mood | **+1.0** |
| Energy closeness: `1 − |song.energy − target_energy|` | **0.0 → +1.0** |
| Acoustic preference aligns (likes_acoustic vs. acousticness ≥ 0.5) | **+0.5** |

Genre is weighted highest because it's the coarsest, most defining bucket of taste; mood is
worth half of that; energy is scored by *proximity* (closest wins, not highest); acoustic
feel is a small tie-breaker. Each rule also records a human-readable **reason** so a
recommendation can be explained (e.g. `"genre match (+2.0)"`).

**Data flow.**

```
User Prefs  →  [loop: score every song with score_song]  →  sort high→low  →  Top K recs
```

**Biases I expect.** Because genre is worth the most points, the system may **over-prioritize
genre** and bury great songs that match the user's mood but not their genre. Exact string
matching also means near-matches like `"pop"` vs. `"indie pop"` score zero for genre even
though they're musically close. Finally, the energy-closeness score quietly favors
**mid-energy songs**, since they're never far from any target.

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

A sample run of `python -m src.main` for the default "Happy Pop" profile:

```
Loaded songs: 18

============================================================
Profile: Happy Pop
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
============================================================
1. Sunrise City — Neon Echo (pop/happy)
   Score: 4.48
   Because: genre match (pop) +2.0; mood match (happy) +1.0; energy close to 0.80 +0.98; non-acoustic feel +0.5

2. Gym Hero — Max Pulse (pop/intense)
   Score: 3.37
   Because: genre match (pop) +2.0; energy close to 0.80 +0.87; non-acoustic feel +0.5

3. Rooftop Lights — Indigo Parade (indie pop/happy)
   Score: 2.46
   Because: mood match (happy) +1.0; energy close to 0.80 +0.96; non-acoustic feel +0.5

4. Neon Heartbeat — Aurora Line (k-pop/happy)
   Score: 2.42
   Because: mood match (happy) +1.0; energy close to 0.80 +0.92; non-acoustic feel +0.5

5. Concrete Dreams — Block Theory (hip-hop/energetic)
   Score: 1.50
   Because: energy close to 0.80 +1.00; non-acoustic feel +0.5
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Diverse profile runs

I stress-tested the recommender with five profiles (defined in `src/main.py`), including an
adversarial one that combines a sad mood with high energy. Top results per profile:

```
Chill Lofi        → 1. Library Rain (lofi/chill) 4.50   2. Midnight Coding (lofi/chill) 4.43
Deep Intense Rock → 1. Storm Runner (rock/intense) 4.49  2. Gym Hero (pop/intense) 2.47
Acoustic Folk     → 1. Paper Boats (folk/sad) 4.50       2. Spacewalk Thoughts (ambient/chill) 1.48
High-Energy Sad   → 1. Neon Horizon (edm/energetic) 3.44 2. Storm Runner (rock/intense) 1.49
```

Each "clean" profile puts its obvious match first by a wide margin. The adversarial profile
has no sad + high-energy song, so the "sad" mood never scores and the result falls back to
genre + energy — the system ignores the part of the request it can't satisfy rather than
breaking. Comparisons are discussed in `model_card.md`.

<details>
<summary>Full terminal output for all five profiles (click to expand)</summary>

```
Loaded songs: 18

============================================================
Profile: Happy Pop
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
============================================================
1. Sunrise City — Neon Echo (pop/happy)
   Score: 4.48
   Because: genre match (pop) +2.0; mood match (happy) +1.0; energy close to 0.80 +0.98; non-acoustic feel +0.5

2. Gym Hero — Max Pulse (pop/intense)
   Score: 3.37
   Because: genre match (pop) +2.0; energy close to 0.80 +0.87; non-acoustic feel +0.5

3. Rooftop Lights — Indigo Parade (indie pop/happy)
   Score: 2.46
   Because: mood match (happy) +1.0; energy close to 0.80 +0.96; non-acoustic feel +0.5

4. Neon Heartbeat — Aurora Line (k-pop/happy)
   Score: 2.42
   Because: mood match (happy) +1.0; energy close to 0.80 +0.92; non-acoustic feel +0.5

5. Concrete Dreams — Block Theory (hip-hop/energetic)
   Score: 1.50
   Because: energy close to 0.80 +1.00; non-acoustic feel +0.5

============================================================
Profile: Chill Lofi
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
============================================================
1. Library Rain — Paper Lanterns (lofi/chill)
   Score: 4.50
   Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy close to 0.35 +1.00; acoustic feel +0.5

2. Midnight Coding — LoRoom (lofi/chill)
   Score: 4.43
   Because: genre match (lofi) +2.0; mood match (chill) +1.0; energy close to 0.35 +0.93; acoustic feel +0.5

3. Focus Flow — LoRoom (lofi/focused)
   Score: 3.45
   Because: genre match (lofi) +2.0; energy close to 0.35 +0.95; acoustic feel +0.5

4. Spacewalk Thoughts — Orbit Bloom (ambient/chill)
   Score: 2.43
   Because: mood match (chill) +1.0; energy close to 0.35 +0.93; acoustic feel +0.5

5. Coffee Shop Stories — Slow Stereo (jazz/relaxed)
   Score: 1.48
   Because: energy close to 0.35 +0.98; acoustic feel +0.5

============================================================
Profile: Deep Intense Rock
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
============================================================
1. Storm Runner — Voltline (rock/intense)
   Score: 4.49
   Because: genre match (rock) +2.0; mood match (intense) +1.0; energy close to 0.90 +0.99; non-acoustic feel +0.5

2. Gym Hero — Max Pulse (pop/intense)
   Score: 2.47
   Because: mood match (intense) +1.0; energy close to 0.90 +0.97; non-acoustic feel +0.5

3. Neon Heartbeat — Aurora Line (k-pop/happy)
   Score: 1.48
   Because: energy close to 0.90 +0.98; non-acoustic feel +0.5

4. Neon Horizon — Pulse Factory (edm/energetic)
   Score: 1.44
   Because: energy close to 0.90 +0.94; non-acoustic feel +0.5

5. Iron Verdict — Ragefall (metal/aggressive)
   Score: 1.43
   Because: energy close to 0.90 +0.93; non-acoustic feel +0.5

============================================================
Profile: Acoustic Folk
Prefs:   {'genre': 'folk', 'mood': 'sad', 'energy': 0.3, 'likes_acoustic': True}
============================================================
1. Paper Boats — Ander Fields (folk/sad)
   Score: 4.50
   Because: genre match (folk) +2.0; mood match (sad) +1.0; energy close to 0.30 +1.00; acoustic feel +0.5

2. Spacewalk Thoughts — Orbit Bloom (ambient/chill)
   Score: 1.48
   Because: energy close to 0.30 +0.98; acoustic feel +0.5

3. Library Rain — Paper Lanterns (lofi/chill)
   Score: 1.45
   Because: energy close to 0.30 +0.95; acoustic feel +0.5

4. Winter Sonata — Adagio Hall (classical/dreamy)
   Score: 1.45
   Because: energy close to 0.30 +0.95; acoustic feel +0.5

5. Coffee Shop Stories — Slow Stereo (jazz/relaxed)
   Score: 1.43
   Because: energy close to 0.30 +0.93; acoustic feel +0.5

============================================================
Profile: Adversarial: High-Energy Sad
Prefs:   {'genre': 'edm', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}
============================================================
1. Neon Horizon — Pulse Factory (edm/energetic)
   Score: 3.44
   Because: genre match (edm) +2.0; energy close to 0.90 +0.94; non-acoustic feel +0.5

2. Storm Runner — Voltline (rock/intense)
   Score: 1.49
   Because: energy close to 0.90 +0.99; non-acoustic feel +0.5

3. Neon Heartbeat — Aurora Line (k-pop/happy)
   Score: 1.48
   Because: energy close to 0.90 +0.98; non-acoustic feel +0.5

4. Gym Hero — Max Pulse (pop/intense)
   Score: 1.47
   Because: energy close to 0.90 +0.97; non-acoustic feel +0.5

5. Iron Verdict — Ragefall (metal/aggressive)
   Score: 1.43
   Because: energy close to 0.90 +0.93; non-acoustic feel +0.5
```

</details>

### Weight experiment

I halved the genre weight (2.0 → 1.0) and doubled the energy weight (1.0 → 2.0) for the Happy
Pop profile:

```
Baseline (genre 2.0, energy 1.0):   1. Sunrise City  2. Gym Hero        3. Rooftop Lights
Experiment (genre 1.0, energy 2.0): 1. Sunrise City  2. Rooftop Lights  3. Neon Heartbeat  (Gym Hero → #4)
```

"Gym Hero" (pop/intense) dropped from #2 to #4 while the happy-mood tracks rose. The change
made the results *different*, not clearly better — it traded "same genre" for "right mood +
energy," showing how sensitive the ranking is to the weights.

---

## Limitations and Risks

- It works on a tiny 18-song catalog, so the top results have little variety and one strong
  feature (like energy) can dominate many different profiles.
- Genre matching is exact, so musically-close genres ("pop" vs. "indie pop") are treated as
  unrelated and score zero.
- It doesn't understand lyrics, language, artist popularity, or listening history — whole
  dimensions of real taste are missing.
- Most moods appear on only one or two songs, so a mood preference often contributes nothing.

I go deeper on these in the [model card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made "recommendation" feel a lot less magical. Under the hood it's just **scoring
plus sorting**: a rule turns each song's features into a number, and ranking picks the highest.
Once I saw that, I understood how a recommender turns plain data (genre, mood, energy) into a
prediction about what someone will like — it's a formula, and the choices inside that formula
do all the work.

That's also where bias sneaks in. The weights aren't neutral: because genre is worth the most
points, the system quietly favors users whose taste sits in a well-represented genre and
sidelines everyone else. With a small catalog, one strong feature (energy) kept pushing the
same song to the top of very different profiles — a mini "filter bubble." In a real system,
those same design choices — which features count, how they're weighted, whose data is in the
catalog — decide what millions of people do and don't get to hear.



