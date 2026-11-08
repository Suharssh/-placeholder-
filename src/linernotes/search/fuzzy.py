"""Fuzzy string similarity, written by hand first (that's the learning).

Afterwards, compare your results and speed against `rapidfuzz` (RESOURCES.md).
If you switch, keep these function names as a thin wrapper so index.py
doesn't care which one runs underneath.
"""

from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    """Minimum single-character insertions/deletions/substitutions to turn a into b.

    Classic dynamic programming. Start with the full (len(a)+1) x (len(b)+1) table,
    get the tests green, then reduce memory to two rows. Complexity: O(len(a)*len(b)).

    Stretch: Damerau-Levenshtein (adjacent transpositions count as 1). "mnoey"
    for "money" is the kind of typo people actually make.
    """
    if len(a) < len(b):
        a, b = b, a  # keep the row as short as possible
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def similarity(a: str, b: str) -> float:
    """Edit distance turned into a score in [0.0, 1.0]; 1.0 means identical.

    Common choice: 1 - levenshtein(a, b) / max(len(a), len(b)).
    Define the empty-string cases explicitly (both empty -> 1.0?).
    """
    longest = max(len(a), len(b))
    if longest == 0:
        return 1.0
    return 1.0 - levenshtein(a, b) / longest


def prefix_score(query: str, candidate: str) -> float:
    """How well `query` works as a typed-so-far prefix of `candidate`.

    This is what makes search-as-you-type feel right: "mon" should rank
    "Money Trees" highly even though the edit distance is large.
    Ideas: exact prefix of the whole string; prefix of any token
    ("tre" -> "money TREes"); weight earlier tokens higher.
    """
    if not query:
        return 0.0
    if candidate.startswith(query):
        return 0.5 + 0.5 * len(query) / len(candidate)
    for word in candidate.split()[1:]:
        if word.startswith(query):
            return 0.4 + 0.4 * len(query) / len(word)
    return 0.0


def score(query: str, candidate: str) -> float:
    """The single number the index ranks by. Inputs are already normalized.

    DECISION D6: how to combine signals. A starting point:
        exact match           -> 1.0
        prefix_score          -> high weight (as-you-type)
        token-level similarity -> medium (handles word order, "trees money")
        whole-string similarity -> low (handles typos)
    Take a weighted max or a weighted sum? Try both against the test
    queries and keep a small table of results in your ADR. That table *is* the
    argument for your decision.
    """
    if query == candidate:
        return 1.0
    words = candidate.split() or [candidate]
    return max(
        prefix_score(query, candidate),
        0.8 * max(similarity(query, w) for w in words),
        0.6 * similarity(query, candidate),
    )
