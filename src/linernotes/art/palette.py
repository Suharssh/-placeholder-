"""Palettes: the colours YOU choose, loaded from palettes/*.toml.

File format (see palettes/mine.toml):

    name = "mono"
    background = "#000000"
    [ramps]
    mono = ["#000000", "#ffffff"]   # dark -> light
    [ui]                            # optional, UI-only colours (never used by the art)
    dim = "#3a3a3a"

The current palette is two colours. The code stays general (N colours, ramps)
so you can try other palettes later without rewriting anything. The quantizer
only needs the flat colour list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

RGB = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class Palette:
    name: str
    colors: tuple[RGB, ...]                                   # art colours: flat, de-duplicated, stable order
    ramps: dict[str, tuple[RGB, ...]] = field(default_factory=dict)
    ui: dict[str, RGB] = field(default_factory=dict)         # UI-only extras, e.g. {"dim": ...}
    explicit_background: RGB | None = None

    @property
    def background(self) -> RGB:
        """Screen colour around the art. The explicit `background` key if set, else the darkest colour.

        "Darkest" needs a lightness measure: use colorspace.luminance.
        """
        raise NotImplementedError

    @property
    def foreground(self) -> RGB:
        """The lightest art colour. In a 1-bit palette this is the "ink" (white on black)."""
        raise NotImplementedError

    @property
    def is_one_bit(self) -> bool:
        """True when there are exactly two art colours. The pipeline uses this
        to switch to the faster grayscale + threshold/dither path."""
        raise NotImplementedError


def parse_hex(value: str) -> RGB:
    """'#ff8800' or 'ff8800' or '#f80' -> (255, 136, 0).

    Raise ValueError on anything else, with the bad value in the message.
    """
    raise NotImplementedError


def to_hex(rgb: RGB) -> str:
    """(255, 136, 0) -> '#ff8800'. Textual/Rich styles accept this form."""
    raise NotImplementedError


def load_palette(path: Path) -> Palette:
    """Read a palette TOML file with stdlib `tomllib`.

    tomllib.load() takes a file opened in BINARY mode; tomllib.loads() takes a str.
    Validate: at least 2 colours, every entry parses, ramps non-empty.
    Flatten ramps into `colors` in file order, dropping duplicates.
    Parse the optional `background` key and `[ui]` table.
    """
    raise NotImplementedError


def palette_from_image(path: Path, n_colors: int) -> Palette:
    """Starting point only: pull `n_colors` representative colours from an image.

    Not needed for the 1-bit palette. Useful if you later experiment with
    more colours. Algorithms to learn: median cut, k-means in OKLab, or
    Pillow's Image.quantize(colors=n) followed by getpalette().
    """
    raise NotImplementedError
