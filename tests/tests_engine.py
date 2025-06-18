import pytest
from engine.core import get_random_words, evaluate_typing

@pytest.fixture
def sample_words():
    return ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta"]

# === get_random_words ===

def test_get_random_words_returns_correct_length(sample_words):
    result = get_random_words(sample_words, count=4)
    assert len(result) == 4

def test_get_random_words_all_in_source(sample_words):
    result = get_random_words(sample_words, count=5)
    assert all(word in sample_words for word in result)

# === evaluate_typing ===

def test_evaluate_typing_all_correct():
    expected = ["apple", "banana", "cherry"]
    typed = ["apple", "banana", "cherry"]
    time_taken = 30
    result = evaluate_typing(typed, expected, time_taken)
    assert result["correct"] == 3
    assert result["total_words"] == 3
    assert result["accuracy"] == 100.0
    assert result["wpm"] > 0

def test_evaluate_typing_some_incorrect():
    expected = ["apple", "banana", "cherry"]
    typed = ["apple", "berry", "cherry"]
    time_taken = 60
    result = evaluate_typing(typed, expected, time_taken)
    assert result["correct"] == 2
    assert result["total_words"] == 3
    assert 0 < result["accuracy"] < 100.0

def test_evaluate_typing_empty_input():
    result = evaluate_typing([], [], 30)
    assert result["correct"] == 0
    assert result["total_words"] == 0
    assert result["accuracy"] == 0.0
