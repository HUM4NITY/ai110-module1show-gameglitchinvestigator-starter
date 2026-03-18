import random
import streamlit as st
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    guess_temperature,
    load_high_score,
    parse_guess,
    save_high_score,
    update_score,
    validate_guess_in_range,
)


def start_new_game(difficulty: str):
    """Reset game state for a given difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.sidebar.caption(f"Best score: {st.session_state.get('high_score', 0)}")

if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score()

if "difficulty" not in st.session_state:
    start_new_game(difficulty)

if st.session_state.difficulty != difficulty:
    # FIXME: Logic breaks here when difficulty changes and old secret stays active.
    start_new_game(difficulty)
    st.info("Difficulty changed. New round started with an updated range.")
    st.rerun()

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key="guess_input"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: Refactored reset flow with Copilot-guided extraction into start_new_game.
    start_new_game(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    else:
        in_range, range_err = validate_guess_in_range(guess_int, low, high)
        if not in_range:
            st.error(range_err)
            st.stop()

        # FIXME: Logic breaks here when attempts increment before parsing/range checks.
        st.session_state.attempts += 1
        outcome, message = check_guess(guess_int, st.session_state.secret)
        temp_label = guess_temperature(guess_int, st.session_state.secret)

        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.warning(f"{message} | Heat check: {temp_label}")
            else:
                st.info(f"{message} | Heat check: {temp_label}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        st.session_state.history.append(
            {
                "attempt": st.session_state.attempts,
                "guess": guess_int,
                "outcome": outcome,
                "temperature": temp_label,
                "score": st.session_state.score,
            }
        )

        if outcome == "Win":
            # FIX: Added persistent high-score tracking with AI-assisted multi-file changes.
            st.session_state.high_score = save_high_score(st.session_state.score)
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.history:
    st.subheader("Guess History")
    st.table(st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
