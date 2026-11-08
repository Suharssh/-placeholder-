"""Settings: every path and tunable lives here, not scattered through the code."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

DitherMode = Literal["none", "ordered", "atkinson", "floyd-steinberg"]
Encoding = Literal["half", "quadrant", "braille"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable app configuration.

    DECISION (ARCHITECTURE.md D3): why frozen? Think about what could go wrong if
    a screen mutated settings mid-session, and how you would "change palette" at
    runtime if you later want that (hint: dataclasses.replace).
    """

    project_root: Path
    catalog_path: Path
    assets_dir: Path          # artist source images live here (you pick them)
    palettes_dir: Path
    cache_dir: Path           # rendered art cache (see art/cache.py)
    palette_name: str = "mine"
    dither: DitherMode = "atkinson"   # D8
    art_encoding: Encoding = "half"   # D2
    art_margin_cells: int = 2         # minimum gap between art and terminal edge
    use_cache: bool = True


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from `start` (default: this file) until a dir containing pyproject.toml.

    Why this exists: so `python -m linernotes` works no matter which directory
    you launch it from. Alternative to research: importlib.resources (what you
    would use once the package is installed somewhere else).
    """
    raise NotImplementedError


def load_settings(
    *,
    catalog: str | None = None,
    palette: str | None = None,
    dither: DitherMode | None = None,
    use_cache: bool | None = None,
) -> Settings:
    """Build Settings from defaults, overridden by any non-None argument.

    Optional stretch: also read overrides from environment variables
    (e.g. LINERNOTES_PALETTE). Decide precedence: CLI > env > defaults.
    """
    raise NotImplementedError
