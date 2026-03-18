# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🎯 Game Purpose

This project is a Streamlit number-guessing game where players choose a difficulty,
submit guesses, and get directional hints until they win or run out of attempts.
The mission in this lab was to investigate real bugs in AI-generated code,
repair the logic safely, and verify those repairs with tests.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🐞 Bugs Found (Expected vs Actual)

1. Reversed hint text:
   - Expected: if guess is above secret, hint should say go lower.
   - Actual: game returned `"Too High"` with a `"Go HIGHER!"` hint.
2. Attempt/score instability:
   - Expected: invalid input should not consume an attempt.
   - Actual: attempts incremented before parsing, so blank/invalid guesses still reduced remaining turns.
3. Difficulty/range state mismatch:
   - Expected: game range and secret should match selected difficulty.
   - Actual: new game reset secret with `random.randint(1, 100)` regardless of difficulty.
4. Missing refactor target:
   - Expected: core logic reusable from `logic_utils.py`.
   - Actual: `logic_utils.py` had `NotImplementedError` stubs and tests failed immediately.

## ✅ Fixes Applied

1. Refactored all core logic into `logic_utils.py`:
   - Implemented `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score`.
2. Corrected game rules and hints:
   - Fixed high/low hint text and removed mixed string/int comparisons.
3. Fixed state flow in `app.py`:
   - Added a `start_new_game` reset path that always honors current difficulty range.
   - Increment attempts only after valid, in-range guesses.
4. Added meaningful feature expansion:
   - Persistent high score saved to `high_score.json`.
   - Guess history table with attempt, outcome, temperature, and score.

## 📝 Document Your Experience

- [x] Described the game's purpose.
- [x] Detailed bugs found with expected vs actual behavior.
- [x] Explained fixes and why they work.

## 🧪 Testing Evidence

- Starter tests initially failed with `NotImplementedError` from `logic_utils.py`.
- After fixes, pytest passes:
   - `8 passed in 0.08s`
- Added edge-case tests for:
   - non-numeric input,
   - decimal input,
   - negative out-of-range guesses,
   - empty input.

## 📸 Demo

- [ ] Insert screenshot: winning game screen after fixes
- [ ] Insert screenshot: pytest run showing all tests passing

## 🤖 AI Collaboration Notes

- Correct AI guidance used:
   - Refactor game logic into `logic_utils.py` and import into `app.py`.
   - Verify behavior with targeted pytest cases after each fix.
- Misleading AI guidance rejected:
   - Suggestion to cast values to strings in `check_guess` to "avoid type errors".
   - Rejected because it can produce lexicographic comparisons and wrong outcomes.

## 🚀 Stretch Features

- [x] Challenge 1: Advanced Edge-Case Testing (added 4 edge-case tests)
- [x] Challenge 2: Feature Expansion via Agent Mode concept (persistent high score + guess history)
- [x] Challenge 3: Professional Documentation and Style (full docstrings + PEP 8-friendly cleanup)
- [ ] Challenge 4: Enhanced Game UI screenshot (optional)
- [ ] Challenge 5: AI model comparison write-up (optional)
