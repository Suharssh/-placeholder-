"""One call the UI makes: "give me this artist's art for a box this big"."""

from __future__ import annotations

from pathlib import Path

from linernotes.art.cache import ArtCache
from linernotes.art.palette import Palette
from linernotes.art.pixelate import DitherMode
from linernotes.art.render import CellGrid, Encoding


def pixel_size_for_box(cols: int, rows: int, encoding: Encoding = "half") -> tuple[int, int]:
    """Terminal box (cols x rows) -> pixel grid size, via render.pixels_per_cell.

    half 40x20 -> 40x40 px · quadrant -> 80x40 px · braille -> 80x80 px.
    Notice quadrant: 80x40 px fills a box that is physically square. Its pixels
    are tall. The image still looks right, because downscale() squashes it into
    that grid and the terminal stretches it back.
    """
    raise NotImplementedError


def render_art(
    image_path: Path,
    palette: Palette,
    cols: int,
    rows: int,
    *,
    encoding: Encoding = "half",
    dither: DitherMode = "atkinson",
    cache: ArtCache | None = None,
) -> CellGrid:
    """load -> crop to the BOX's physical aspect -> pixelate to pixel_size_for_box -> to_cells.

    Physical aspect of the box = cols / (2 * rows) (cells are 1:2).
    CPU work: runs in a Textual worker thread, never on the event loop. Keep it
    pure and thread-safe: no globals, no UI calls. (ARCHITECTURE.md D4)
    """
    raise NotImplementedError
