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

Real recommenders like Spotify and YouTube learn what you like by watching what you play, save, and skip, then mixing a few signals together: what similar listeners enjoy, what a song actually sounds like, and how people describe it. My version is a much smaller, simpler take on the same idea. Instead of learning from millions of users, it compares each song directly against a user's stated taste and prioritizes the most obvious matches first. Genre and mood come first, then how close the song's energy is to what the user wants, with acoustic-ness as a tie-breaker. The goal isn't to be clever. It's to be predictable and easy to explain, so you can always see why a song was recommended.

**What each `Song` uses:** every song has a genre, mood, and four 0-1 features (energy, valence, danceability, acousticness) plus tempo. The scorer only looks at genre, mood, energy, and acousticness. The rest are along for the ride for now.

**What the `UserProfile` stores:** four things, one per feature the scorer compares against: `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`.

**How a score is computed:** each song is judged on its own and earns points for matching the user. Then every song is ranked by its total and the top K come back.

### Algorithm Recipe

```
+2.0   genre matches favorite_genre
+1.0   mood matches favorite_mood
+X     energy closeness, where X = 1 - |target_energy - song energy|   (0.0 to 1.0)
+0.5   acousticness side (>0.5?) matches likes_acoustic
------
 max 4.5 points, then sort high to low and take the top K
```

The idea behind the weights: genre is the clearest thing a listener asks for, so it counts most. Mood is worth half a genre. Energy is continuous, so it acts as a tie-breaker between songs that already matched. Acousticness is a small final nudge.

**Data flow:** user prefs + songs.csv go in, the loop scores every song one at a time, then the ranking sorts them and returns the top K.

**Biases I expect:** this system leans hard on genre. A song that perfectly matches your mood and energy but sits in a different genre can lose to a so-so song that happens to share your genre, so great cross-genre picks get buried. It also only rewards exact genre and mood matches, so a user who likes "rock" gets nothing extra for a metal or punk track that a real listener would love. And with a tiny catalog, a rare genre choice leaves the ranking decided almost entirely by the energy number, which is a much blurrier signal.

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

A sample run of the recommender for a pop, happy, high-energy listener:

```
Loaded songs: 18

============================================
  Top 5 picks for you
  genre=pop  mood=happy  energy=0.8
============================================

  1. Sunrise City - Neon Echo
     score: 3.98
     why:   matches your favorite genre (pop); matches your mood (happy); very close to your energy level

  2. Gym Hero - Max Pulse
     score: 2.87
     why:   matches your favorite genre (pop); very close to your energy level

  3. Rooftop Lights - Indigo Parade
     score: 1.96
     why:   matches your mood (happy); very close to your energy level

  4. Concrete Kings - Vell Rhymes
     score: 0.98
     why:   very close to your energy level

  5. Night Drive Loop - Neon Echo
     score: 0.95
     why:   very close to your energy level
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



