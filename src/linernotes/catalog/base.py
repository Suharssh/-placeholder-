"""The Catalog *port*: what the rest of the app needs from a data source.

Read about "ports and adapters" (RESOURCES.md) before touching this. The point:
the UI and search code depend on this Protocol, never on JSON, SQLite or an HTTP
API. A different data source later means a new adapter, with no UI changes.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from linernotes.domain import Artist


class CatalogError(Exception):
    """Raised for missing/invalid catalog data (bad file, unknown id, ...)."""


class Catalog(Protocol):
    """Read-only access to artists.

    DECISION D10: sync or async? Local file, so sync is fine. A network-backed
    catalog would want `async def`. Write down what changing this later would cost
    (every caller changes) and decide consciously.
    """

    def artists(self) -> Sequence[Artist]:
        """All artists, in a stable order."""
        ...

    def artist(self, artist_id: str) -> Artist:
        """One artist by id. Raises CatalogError if unknown."""
        ...
