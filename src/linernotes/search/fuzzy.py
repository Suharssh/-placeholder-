"""
This file checks the fuzzy score, since its key stroke based - 

prefix match on every keystroke from the query to actual name
per key matching - unlikely 
exact name - perfect match


"""



from __future__ import annotations


def levenshtein(a: str, b: str) -> int:
    # make `b` the shorter string so each row stays as small as possible
    if len(a) < len(b):
        a, b = b, a

    # first row of the grid: turning "" into b[:j] takes j inserts -> [0, 1, 2, ...]
    prev = list(range(len(b) + 1))

    # walk through `a` one letter at a time (i = 1, 2, ...)
    for i, ca in enumerate(a, 1):
        # first cell of each row: turning a[:i] into "" takes i deletes
        cur = [i]

        # compare this letter of `a` with every letter of `b`
        for j, cb in enumerate(b, 1):
            # cheapest of three moves:
            #   prev[j] + 1          -> delete a letter     (cell above)
            #   cur[j - 1] + 1       -> insert a letter     (cell to the left)
            #   prev[j - 1] + (ca != cb) -> substitute: free if letters match, else 1 (diagonal)
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))

        # only the previous row is ever needed, so drop the rest of the grid
        prev = cur

    # bottom-right cell = minimum edits to turn a into b: "kendrik" -> "kendrick" = 1
    return prev[-1]


def similarity(a: str, b: str) -> float:
    # length of the longer string, used to scale the edit count
    longest = max(len(a), len(b))

    # two empty strings are identical
    if longest == 0:
        return 1.0

    # turn edits into a 0..1 score: 0 edits -> 1.0, all letters different -> 0.0
    # dividing by length makes 1 typo in a short name count more than in a long one
    return 1.0 - levenshtein(a, b) / longest


def prefix_score(query: str, candidate: str) -> float:
    # nothing typed yet -> no prefix match
    if not query:
        return 0.0

    # whole name starts with the query: "kend" -> "kendrick lamar" (strongest signal)
    # base 0.5 + bonus for how much of the name has been typed
    if candidate.startswith(query):
        return 0.5 + 0.5 * len(query) / len(candidate)

    # a later word starts with the query: "lam" -> "kendrick lamar"
    # first word skipped: the startswith check above already covered it
    for word in candidate.split()[1:]:
        if word.startswith(query):
            # slightly lower base (0.4) than a whole-name prefix, bonus for how much of the word is typed
            return 0.4 + 0.4 * len(query) / len(word)

    # not a prefix of the name or any word
    return 0.0


def score(query: str, candidate: str) -> float:
    # exact match always wins: "kdot" -> "kdot"
    if query == candidate:
        return 1.0

    # split the name into words for per-word typo matching ("" -> [""] so max() never sees an empty list)
    words = candidate.split() or [candidate]

    # take the strongest signal (max, not sum: one good reason to match is enough)
    return max(
        # still typing: "kend" -> "kendrick lamar"
        prefix_score(query, candidate),
        # typo in one word: "lamarr" -> "lamar" (weighted 0.8)
        0.8 * max(similarity(query, w) for w in words),
        # typo across the whole name: "kendrik lamar" -> "kendrick lamar" (weighted 0.6)
        0.6 * similarity(query, candidate),
    )