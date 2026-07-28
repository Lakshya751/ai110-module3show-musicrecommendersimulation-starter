# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
