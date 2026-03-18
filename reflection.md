# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first run launched in Streamlit, but gameplay behavior was inconsistent and hard to trust. I opened the Developer Debug Info panel and compared the secret number with the hints, and I saw clear contradictions. For example, when my guess was higher than the secret, the game reported "Too High" but still told me to go higher, which is the opposite of expected behavior. I also found that attempts were consumed even when input was invalid, because the counter incremented before parsing and range validation. A third bug was that difficulty/range state was inconsistent: reset logic used a fixed `1..100` secret range even when the selected difficulty was not Normal.

---

## 2. How did you use AI as a teammate?

I used Copilot chat and code-aware prompts focused on `app.py`, `logic_utils.py`, and `tests/test_game_logic.py`. One correct suggestion was to extract all game logic into `logic_utils.py` and keep `app.py` focused on UI/state flow; this made the code testable and removed duplicated logic paths. I verified that suggestion by running pytest before and after the refactor, and by confirming all logic functions were imported from `logic_utils.py` instead of defined in `app.py`. One misleading suggestion I encountered was to convert values to strings in `check_guess` to avoid type errors; I rejected that because string comparison can create wrong ordering behavior (lexicographic vs numeric). I verified the rejection by keeping numeric comparisons and adding tests that assert correct high/low outcomes.

---

## 3. Debugging and testing your fixes

I considered a bug fixed only when both automated tests and runtime behavior agreed. I first ran pytest and confirmed the starter state failed (`NotImplementedError` from stubbed logic functions), then rebuilt tests to match the real return contracts. I added edge-case tests for empty input, non-numeric strings, decimal input, and negative out-of-range guesses to prove input handling was stable. After implementing fixes, pytest reported `8 passed`, and Streamlit launched successfully with the fixed app (`Local URL: http://localhost:8502`). AI helped me design targeted tests by proposing specific scenarios, but I still validated each expectation against actual game rules before accepting it.

---

## 4. What did you learn about Streamlit and state?

I would explain Streamlit reruns as "the script executes top-to-bottom again on every interaction." That means normal local variables are recalculated unless values are stored in `st.session_state`. For games, this matters a lot because secret number, attempts, and score must persist across reruns to keep gameplay consistent. I learned that reset logic should be centralized in one function so every rerun path uses the same state contract. I also learned to guard state transitions (like difficulty changes) explicitly, then rerun once to stabilize UI and state.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing a failing test for each bug before trying to fix the implementation, because it keeps the debugging process objective. I also want to keep using narrow, file-specific prompts to AI (for example, focusing on one function and one failing case) instead of broad requests. Next time, I would reject speculative AI fixes faster and ask for a minimal patch tied to a single observed symptom. This project changed how I think about AI-generated code: I now treat AI output as a draft hypothesis, not a trustworthy final answer. The best results came from combining AI speed with manual verification in tests and runtime.

---

## Optional: AI Model Comparison (Challenge 5)

I compared a hint-direction bug fix between two assistants and looked at readability plus explanation quality. Model A provided a compact patch quickly, while Model B gave a clearer explanation of why the bug happened in terms of numeric comparisons and user-facing hint text. The better "Pythonic" fix was the one that removed type coercion and kept explicit integer comparisons in a small function. The best explanation was the one that connected code behavior directly to reproducible gameplay symptoms, not just syntax changes.
