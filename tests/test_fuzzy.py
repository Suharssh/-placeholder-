import pytest

from linernotes.search.fuzzy import levenshtein, prefix_score, score, similarity


@pytest.mark.parametrize(
    "a, b, d",
    [("kitten", "sitting", 3), ("", "abc", 3), ("abc", "", 3), ("same", "same", 0), ("money", "mony", 1)],
)
def test_levenshtein(a, b, d):
    assert levenshtein(a, b) == d


def test_levenshtein_symmetric():
    assert levenshtein("kendrick", "kednrick") == levenshtein("kednrick", "kendrick")


def test_similarity_bounds():
    assert similarity("abc", "abc") == 1.0
    assert 0.0 <= similarity("abc", "xyz") <= 1.0


def test_prefix_beats_typo_for_short_queries():
    # As-you-type: "mon" is a better hint for "money trees" than for "lemon".
    assert prefix_score("mon", "money trees") > prefix_score("mon", "lemon")


def test_token_prefix():
    assert prefix_score("tre", "money trees") > 0


def test_exact_is_best():
    assert score("alright", "alright") >= score("alright", "alright remix")
