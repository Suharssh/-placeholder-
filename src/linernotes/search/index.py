"""SearchIndex: holds searchable items and answers queries.

Generic over the item type: today it's SearchIndex[Artist], and nothing in here
should know that. Anything you want to search later reuses it unchanged.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

from linernotes.search.fuzzy import score
from linernotes.search.normalize import normalize

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

    DECISION D5: option (a), a plain list scored in full on every keystroke.
    Measured: ~18 us per score() call, so a few hundred names cost well under 5 ms.
    """

    def __init__(self, keys: Callable[[T], Iterable[str]]) -> None:
        # how to get the searchable names out of an item (passed in, so the index never knows what an "artist" is)
        self._keys = keys
        # each item stored once; its position in this list is its "item number"
        self._items: list[T] = []
        # one row per NAME: (normalized name, original name, item number)
        # e.g. ("kdot", "K.Dot", 0), ("kendrick lamar", "Kendrick Lamar", 0)
        self._entries: list[tuple[str, str, int]] = []

    def add(self, item: T) -> None:
        # the item's number = where it lands in self._items
        number = len(self._items)
        self._items.append(item)
        # store every name under that number, normalized ONCE here (the stored side of the golden rule)
        for name in self._keys(item):
            normalized = normalize(name)
            if normalized:                       # skip names that normalize to "" (e.g. "...")
                self._entries.append((normalized, name, number))

    def extend(self, items: Iterable[T]) -> None:
        # index many items, one at a time
        for item in items:
            self.add(item)

    def __len__(self) -> int:
        # number of ITEMS (artists), not names: Kendrick counts once, not three times
        return len(self._items)

    def _candidates(self, normalized_query: str) -> Iterable[tuple[str, str, int]]:
        # option (a): everything is a candidate. A trie/n-gram index would only change THIS method.
        return self._entries

    def search(self, query: str, *, limit: int = 8, min_score: float = 0.35) -> list[Match[T]]:
        # 1. normalize what was typed (the typed side of the golden rule)
        q = normalize(query)
        if not q:
            return []                            # empty or only spaces/punctuation -> no results

        # 2 + 3. score every name; keep only each item's BEST (score, original name)
        best: dict[int, tuple[float, str]] = {}
        for normalized_name, original_name, number in self._candidates(q):
            s = score(q, normalized_name)
            if number not in best or s > best[number][0]:
                best[number] = (s, original_name)

        # 4. drop weak matches (everything scores SOMETHING; 0.1 is noise)
        kept = [(s, name, number) for number, (s, name) in best.items() if s >= min_score]

        # 5. sort: highest score first, then shorter name, then alphabetical
        #    -> the same query always gives the same order, so the dropdown never flickers
        kept.sort(key=lambda row: (-row[0], len(row[1]), row[1].casefold()))

        # 6. top `limit`, wrapped as Match objects for the UI
        return [Match(item=self._items[number], score=s, matched_text=name)
                for s, name, number in kept[:limit]]


def highlight_spans(query: str, text: str) -> tuple[tuple[int, int], ...]:
    """Character ranges in `text` that the query matched, for bold in the UI.

    Not implemented yet: returns no spans, so nothing is bolded. Come back after the UI works.
    """
    return ()