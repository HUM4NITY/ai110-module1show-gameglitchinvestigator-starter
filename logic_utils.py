"""Core gameplay logic for the Glitch Investigator guessing game."""

from __future__ import annotations

import json
from pathlib import Path


HIGH_SCORE_PATH = Path("high_score.json")


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive guessing range for a difficulty label."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """Parse user text input into an integer guess with friendly errors."""
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    text = raw.strip()
    if any(char in text for char in [".", ","]):
        return False, None, "Use a whole number only."

    try:
        value = int(text)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def validate_guess_in_range(guess: int, low: int, high: int) -> tuple[bool, str | None]:
    """Validate that a parsed guess falls inside the active difficulty range."""
    if low <= guess <= high:
        return True, None
    return False, f"Guess must be between {low} and {high}."


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare guess to secret and return the outcome and hint message."""
    if guess == secret:
        return "Win", "Correct!"

    if guess > secret:
        return "Too High", "Too high. Try a lower number."

    return "Too Low", "Too low. Try a higher number."


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score with deterministic rules that reward quicker wins."""
    if outcome == "Win":
        points = max(10, 110 - 10 * attempt_number)
        return current_score + points

    if outcome in {"Too High", "Too Low"}:
        return max(0, current_score - 5)

    return current_score


def guess_temperature(guess: int, secret: int) -> str:
    """Classify how close a guess is to the secret number."""
    diff = abs(guess - secret)
    if diff == 0:
        return "On fire"
    if diff <= 3:
        return "Very hot"
    if diff <= 10:
        return "Warm"
    return "Cold"


def load_high_score(path: Path = HIGH_SCORE_PATH) -> int:
    """Load persisted high score, returning 0 when no score exists."""
    if not path.exists():
        return 0

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0

    value = payload.get("high_score", 0)
    return value if isinstance(value, int) and value >= 0 else 0


def save_high_score(score: int, path: Path = HIGH_SCORE_PATH) -> int:
    """Persist and return the best score seen across game sessions."""
    best = max(load_high_score(path), score)
    payload = {"high_score": best}

    try:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError:
        return best

    return best
