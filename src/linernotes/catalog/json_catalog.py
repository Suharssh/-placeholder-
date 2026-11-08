"""Adapter: a hand-curated JSON file (data/catalog.json)."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from linernotes.catalog.base import CatalogError
from linernotes.domain import Artist


class JsonCatalog:
    """Implements the Catalog protocol (structurally; no inheritance needed).

    Load eagerly in __init__ or lazily on first access? Eager is simpler and fails
    fast at startup. Lazy makes startup faster. For a small file, measure before
    you optimise.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        self._artists: dict[str, Artist] = {}
        raise NotImplementedError  # call self._load() or defer it; your choice

    def _load(self) -> None:
        """Read the JSON, validate it, populate self._artists.

        Validation you should do (raise CatalogError with a useful message):
          * duplicate artist ids
          * missing required fields (id, name)
          * `image` set but the file doesn't exist in assets/artists/? Error, warning,
            or allowed (show a placeholder)? Decide.
        Hint: Artist(**raw) breaks on unknown keys. Decide: ignore them, or reject them?
        Remember aliases arrive as JSON lists but the dataclass wants tuples.
        """
        raise NotImplementedError

    def artists(self) -> Sequence[Artist]:
        raise NotImplementedError

    def artist(self, artist_id: str) -> Artist:
        raise NotImplementedError
