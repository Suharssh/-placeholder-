"""Domain models. Plain data, no behaviour that needs I/O, no Textual, no Pillow.

Given to you (not a stub) because every other module's signatures depend on it.
You will probably change it: that's expected. When you do, ask what else breaks,
and whether the tests caught it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Artist:
    id: str                          # stable slug, e.g. "kendrick-lamar"
    name: str                        # display name, e.g. "Kendrick Lamar"
    aliases: tuple[str, ...] = ()    # searchable alternates, e.g. ("K.Dot",)
    image: str | None = None         # file name inside assets/artists/
