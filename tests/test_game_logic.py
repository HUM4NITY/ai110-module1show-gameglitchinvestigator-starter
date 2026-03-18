from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
    validate_guess_in_range,
)


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "lower" in message.lower()


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "higher" in message.lower()


def test_score_rewards_faster_win():
    fast_score = update_score(0, "Win", 1)
    slow_score = update_score(0, "Win", 5)
    assert fast_score > slow_score
    assert slow_score >= 10


def test_edge_case_non_numeric_guess_rejected():
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_edge_case_decimal_guess_rejected():
    ok, value, err = parse_guess("42.5")
    assert ok is False
    assert value is None
    assert err == "Use a whole number only."


def test_edge_case_negative_out_of_range_for_easy():
    low, high = get_range_for_difficulty("Easy")
    in_range, err = validate_guess_in_range(-3, low, high)
    assert in_range is False
    assert err == "Guess must be between 1 and 20."


def test_edge_case_empty_guess_rejected():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."
