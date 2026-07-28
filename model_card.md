# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0** — a small, explainable, content-based music recommender.

---

## 2. Intended Use  

VibeMatch suggests songs from a small catalog that match a user's stated taste — a favorite
genre, a favorite mood, a target energy level, and whether they like acoustic music. For every
suggestion it also explains *why* the song was picked.

It assumes the user can describe their taste as a few simple preferences, and that a good
recommendation is one whose attributes are close to those preferences. It is built for
**classroom exploration** — a teaching tool for understanding how content-based scoring and
ranking work.

**Non-intended use.** It should **not** be used as a real music service or to make decisions
that affect people. The catalog is tiny and hand-made, the weights are picked by hand rather
than learned from data, and there's no user history or fairness checking — so it would give
narrow, biased results in the real world. It is not a benchmark of recommender quality and
shouldn't be presented as one.

---

## 3. How the Model Works  

Think of it like a friendly judge giving each song points. The user says what they like —
a genre, a mood, an energy level, and whether they prefer acoustic songs. Then the judge looks
at every song in the list and hands out points: **2 points if the genre matches**, **1 point
if the mood matches**, up to **1 point for how close the song's energy is** to what the user
wants (a perfect match gets the full point, a big gap gets almost none), and **half a point**
if the song's acoustic feel matches the user's preference. Every song ends up with a total
score, and the highest scores rise to the top of the list.

The genre is worth the most because it's the biggest clue about taste, and energy is scored by
*closeness* rather than "more is better," so someone who wants calm music isn't handed the
loudest track. Compared to the starter code — which just returned the first few songs in the
file without looking at them — this version actually reads each song's features, scores them,
sorts by score, and writes a plain-English reason for every pick.

---

## 4. Data  

The catalog is a single CSV, `data/songs.csv`, with **18 songs**. Each song has a genre, a
mood, and five numeric features on a 0.0–1.0 scale (energy, valence, danceability,
acousticness) plus tempo in BPM. I expanded it from the 10 starter songs by adding 8 more so
there would be real variety to rank. Genres now include pop, indie pop, lofi, rock, metal,
edm, hip-hop, r&b, jazz, classical, country, folk, k-pop, ambient, and synthwave; moods
include happy, chill, intense, energetic, aggressive, nostalgic, romantic, sad, dreamy,
relaxed, focused, and moody.

It's still tiny. Most moods are represented by only one or two songs, there are no lyrics or
language information, no artist popularity, and no listening history — so whole dimensions of
real musical taste (culture, era, personal memories, what your friends listen to) are simply
missing.

---

## 5. Strengths  

The system works best for users whose taste lines up with a genre that's well represented in
the catalog — the Happy Pop, Chill Lofi, Deep Intense Rock, and Acoustic Folk profiles all got
an obvious, correct top pick with a clear point gap over the rest. The energy-closeness rule
captures something real: it cleanly separates calm songs from high-energy ones, so the same
catalog produces very different lists for a "study" user versus a "gym" user. And because every
recommendation comes with its reasons, it's easy to see *why* a song ranked where it did — the
scoring is fully transparent, which is exactly what you want in a teaching model.

---

## 6. Limitations and Bias 

The clearest weakness I found is that **the system leans heavily on an exact genre match**,
which is worth the most points (+2.0). If a user's favorite genre isn't in the catalog, no
song can earn those points, so the ranking collapses to whatever happens to have the closest
energy — the recommendations get generic and interchangeable (you can see this in the
"Acoustic Folk" and adversarial runs, where positions 2–5 are separated by hundredths of a
point). Exact string matching also treats musically-close genres as unrelated: an "indie pop"
song scores **zero** on genre for a "pop" fan even though a human would call them siblings.
The energy score quietly favors **mid-energy songs**, since a value near 0.5 is never far from
any target. Finally, mood is fragile — there are twelve moods but usually only one or two
songs per mood, so a mood preference often contributes nothing simply because no song carries
that exact tag.

---

## 7. Evaluation  

I tested five profiles: **Happy Pop**, **Chill Lofi**, **Deep Intense Rock**, **Acoustic
Folk**, and an **adversarial "High-Energy Sad"** profile that deliberately combines a sad mood
with high energy. For each one I ran `python -m src.main` and checked whether the top result
was the song a human would obviously pick, and whether the reasons made sense.

**What I looked for and found:** the "clean" profiles all put the exactly-matching song first
by a wide margin (e.g. Library Rain leads Chill Lofi at 4.50; Paper Boats leads Acoustic Folk
at 4.50). That matched my intuition.

**Profile comparisons:**

- **Chill Lofi vs. Deep Intense Rock** — the lofi profile fills the top with low-energy,
  acoustic lofi/ambient tracks, while the rock profile pulls high-energy, non-acoustic
  rock/metal/edm songs. This is the energy score doing its job: the same catalog splits
  cleanly into "calm" and "hype" halves depending only on the target energy.
- **Happy Pop vs. Deep Intense Rock** — both are high-energy, but genre and mood pull them
  apart. "Gym Hero" (pop/intense, high energy) shows up highly in *both* lists, which is a
  good illustration of why the same energetic song keeps appearing for very different users:
  it wins the energy points regardless of the genre/mood a user actually asked for.
- **Adversarial High-Energy Sad** — no song is both sad and high-energy, so the "sad" mood
  never scores. The result falls back to genre (edm) + energy, returning "Neon Horizon." The
  system doesn't break on conflicting input; it just quietly ignores the part of the request
  it can't satisfy — which is worth knowing.

**Experiment I ran:** I halved the genre weight (2.0 → 1.0) and doubled the energy weight
(1.0 → 2.0) for the Happy Pop profile. "Gym Hero" (pop/intense) dropped from #2 to #4, while
"Rooftop Lights" and "Neon Heartbeat" (both happy, close energy) rose above it. The change
made the results *different*, not obviously more accurate — it just traded "same genre" for
"right mood + energy," which shows how sensitive the output is to the weights.

**Biggest surprise:** how often the *same* high-energy song surfaces across unrelated
profiles. It taught me that a single strong feature (energy) can dominate when the catalog is
small, which is exactly the kind of "filter bubble" real recommenders have to fight.

---

## 8. Future Work  

- **Softer genre matching.** Give partial credit for related genres (e.g. "pop" and "indie
  pop") instead of an all-or-nothing exact string match, so near-misses aren't scored as zero.
- **A diversity rule.** Penalize the score of a song whose artist or genre already appears near
  the top, so the list doesn't fill up with near-duplicates and one energetic song can't
  dominate every profile.
- **More features and richer preferences.** Fold in valence, danceability, and tempo, and let a
  user weight the features themselves (or pick a "mode" like Genre-First vs. Energy-Focused) to
  handle more complex tastes.

---

## 9. Personal Reflection  

My biggest learning moment was realizing that a recommendation system is basically just scoring and sorting. There isn’t really any magic behind it. The system takes different features, turns them into numbers, and then ranks the options based on those scores.

What surprised me most was seeing the same high-energy song appear for completely different user profiles. That was when the idea of a “filter bubble” really made sense to me. I could actually see how one strong feature, like energy level, could quietly take over the recommendations, especially when the music catalog was small.

Using AI tools helped me move faster through some of the more repetitive parts, like loading the CSV file, setting up the scoring function, and formatting the terminal output. But I still had to carefully check the parts that controlled the actual logic. Things like the energy-closeness calculation, the weights given to each feature, and the import and file-path setup all mattered, especially when I was trying to get the tests to pass.

This project also changed the way I think about music apps. A system that feels like it “knows me” may actually be using a fairly simple formula supported by a huge amount of data. The decisions behind that formula—what features matter and how much weight each one gets can quietly control what I discover and what I may never get the chance to hear.