import pytest

from linernotes.search.normalize import normalize, tokenize


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Money Trees", "money trees"),
        ("  money   TREES  ", "money trees"),
        ("Beyoncé", "beyonce"),
        ("DNA.", "dna"),
    ],
)
def test_basic(raw, expected):
    assert normalize(raw) == expected


def test_dots_are_deleted_not_spaced():
    # DECISION encoded here: "m.A.A.d" should match someone typing "maad".
    # Changed your mind? Edit this test and record why in an ADR.
    assert normalize("m.A.A.d city") == normalize("maad city")


@pytest.mark.parametrize("raw", ["Money Trees", "Beyoncé", "4 Your Eyez Only", "AC/DC", ""])
def test_idempotent(raw):
    once = normalize(raw)
    assert normalize(once) == once


def test_tokenize():
    assert tokenize(normalize("Money Trees")) == ["money", "trees"]
    assert tokenize("") == []
