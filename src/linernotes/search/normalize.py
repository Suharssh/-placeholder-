"""Text normalization: make "Beyoncé", "BEYONCE" and "beyonce " compare equal.

Every string goes through the SAME normalize() at index time and at query time.
If they ever differ, search silently breaks. That invariant matters more than
any clever scoring.
"""

from __future__ import annotations


def normalize(text: str) -> str:
    """Return a canonical, comparison-ready form of `text`.

    Steps to consider (order matters; think about why):
      1. Unicode normalize (unicodedata.normalize, NFKD) and drop combining marks
         -> "Beyoncé" becomes "Beyonce".
      2. casefold() (not lower(): look up the difference).
      3. Punctuation policy. "m.A.A.d city", "DNA.", "N.Y. State of Mind", "AC/DC".
         Delete punctuation, or replace it with a space? The tests in
         tests/test_normalize.py assume "delete dots, everything else -> space".
         If you choose differently, change the test and write down why.
      4. "&" vs "and"? "feat." / "ft."? Your call; start simple.
      5. Collapse runs of whitespace and strip.

    Must be idempotent: normalize(normalize(x)) == normalize(x).
    """
    raise NotImplementedError


def tokenize(text: str) -> list[str]:
    """Split already-normalized text into tokens.

    "money trees" -> ["money", "trees"]. Trivial now. It's a separate function so
    you can later add stop-words ("the", "a") or stemming in exactly one place.
    """
    raise NotImplementedError
