"""Adapter: a hand-curated JSON file (data/catalog.json)."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

from linernotes.catalog.base import CatalogError
from linernotes.domain import Artist


class JsonCatalog:
    """Implements the Catalog protocol: artists() and artist(id), backed by a JSON file."""

    def __init__(self, path: Path) -> None:
        # where the JSON file lives
        self._path = path
        # artists by id, e.g. {"kendrick-lamar": Artist(...)}; dicts keep insertion (file) order
        self._artists: dict[str, Artist] = {}
        # load eagerly: a broken file fails right here, at startup, with a clear message
        self._load()

    def _load(self) -> None:
        # read the whole file; utf-8 so "Beyoncé" survives on Windows
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise CatalogError(f"catalog not found: {self._path}") from None
        except json.JSONDecodeError as e:
            raise CatalogError(f"catalog is not valid JSON ({self._path}): {e}") from None

        # the file must look like {"artists": [ {...}, {...} ]}
        entries = raw.get("artists") if isinstance(raw, dict) else None
        if not isinstance(entries, list):
            raise CatalogError(f'catalog must contain an "artists" list: {self._path}')

        for n, entry in enumerate(entries, 1):
            # every artist needs an id and a name; report WHICH entry is broken
            if not isinstance(entry, dict) or "id" not in entry or "name" not in entry:
                raise CatalogError(f"artist #{n} is missing 'id' or 'name'")

            # two artists with the same id would silently overwrite each other
            artist_id = entry["id"]
            if artist_id in self._artists:
                raise CatalogError(f"duplicate artist id: {artist_id!r}")

            # build the Artist; JSON lists become tuples (Artist is frozen = unchangeable)
            self._artists[artist_id] = Artist(
                id=artist_id,
                name=entry["name"],
                aliases=tuple(entry.get("aliases", ())),
                image=entry.get("image"),
            )

    def artists(self) -> Sequence[Artist]:
        # every artist, in the order they appear in the file
        return list(self._artists.values())

    def artist(self, artist_id: str) -> Artist:
        # one artist by id; hide the dict's KeyError behind the catalog's own error type
        try:
            return self._artists[artist_id]
        except KeyError:
            raise CatalogError(f"unknown artist id: {artist_id!r}") from None