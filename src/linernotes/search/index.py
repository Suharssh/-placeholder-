"""SearchIndex: holds searchable items and answers queries.

Generic over the item type: today it's SearchIndex[Artist], and nothing in here
should know that. Anything you want to search later reuses it unchanged.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Match(Generic[T]):
    item: T
    score: float                      # 0.0..1.0, higher is better
    matched_text: str                 # which name/alias produced the best score
    spans: tuple[tuple[int, int], ...] = ()  # (start, end) in matched_text, for highlighting


class SearchIndex(Generic[T]):
    """Index items by one or more searchable strings each.

    `keys` maps an item to all strings it should be found by, e.g.
        lambda a: (a.name, *a.aliases)

    DECISION D5: the data structure. Options, simplest first:
      (a) A list of (normalized_key, item). Score every entry on every keystroke.
          With a few thousand artists this is fast enough. MEASURE it (timeit).
      (b) A prefix trie over tokens, to find prefix candidates without a full scan.
      (c) An n-gram (e.g. trigram) inverted index for typo-tolerant candidate lookup,
          then score only the candidates.
      (d) A BK-tree for "everything within edit distance k".
    Implement (a) first. Implement (b) or (c) only if you measured a reason to,
    or because you want to learn it (also a valid reason; write that down).
    """

    def __init__(self, keys: Callable[[T], Iterable[str]]) -> None:
        self._keys = keys
        raise NotImplementedError  # set up your internal storage here

    def add(self, item: T) -> None:
        """Index one item under every string `keys(item)` returns (normalized)."""
        raise NotImplementedError

    def extend(self, items: Iterable[T]) -> None:
        """Index many items. Fine to just loop over add()."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Number of distinct items (not keys)."""
        raise NotImplementedError

    def _candidates(self, normalized_query: str) -> Iterable[tuple[str, T]]:
        """Return (key, item) pairs worth scoring. With option (a): everything."""
        raise NotImplementedError

    def search(self, query: str, *, limit: int = 8, min_score: float = 0.35) -> list[Match[T]]:
        """Top `limit` matches for `query`, best first.

        Rules the tests check:
          * Empty / whitespace-only query -> [] (or all items? decide; tests say []).
          * An item matched by several keys appears ONCE, with its best score.
          * Results below `min_score` are dropped.
          * Deterministic tie-breaking (e.g. by shorter key, then alphabetical)
            so the list doesn't shuffle while the user types.
        """
        raise NotImplementedError


def highlight_spans(query: str, text: str) -> tuple[tuple[int, int], ...]:
    """Character ranges in `text` that the query matched, for bold/colour in the UI.

    Careful: `text` is the ORIGINAL display string, but you matched on the
    normalized one. Mapping positions back is the interesting part. Start by
    returning () and come back to this after the UI works.
    """
    raise NotImplementedError
