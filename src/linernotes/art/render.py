"""Pixel grid -> terminal cells.

A terminal cell is about twice as tall as it is wide. Several Unicode tricks
pack more than one "pixel" into a cell:

  encoding  pixels/cell  glyphs                      colours per cell
  half      1 x 2        ▀ ▄ █ (space)               2 (fg + bg), any colours
  quadrant  2 x 2        ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█ (space)     2
  braille   2 x 4        U+2800..U+28FF (⠁ ... ⣿)    2

With a full-colour palette, half blocks win (every pixel keeps its exact
colour). With a BLACK-AND-WHITE palette the 2-colours-per-cell limit costs
nothing, so quadrant (2x the pixels) and braille (4x) become real options.

DECISION D2:
  * half: chunky, square pixels. The "pixel art" look of your first reference.
  * braille: 4x the resolution, dots with gaps between them. Reads as a
    fine dot-matrix print.
  * quadrant: 2x the resolution, but its pixels are 1:2 TALL rectangles
    (not square). Works, looks odd on diagonals.
Render the same portrait all three ways (scripts/preview_art.py --compare-encoding)
and decide with your eyes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from PIL import Image

from linernotes.art.palette import RGB

Encoding = Literal["half", "quadrant", "braille"]

UPPER_HALF = "▀"  # ▀
LOWER_HALF = "▄"  # ▄
FULL_BLOCK = "█"  # █
BRAILLE_BASE = 0x2800  # empty braille cell; add dot bits to get the glyph


@dataclass(frozen=True, slots=True)
class Cell:
    char: str
    fg: RGB | None
    bg: RGB | None


CellGrid = list[list[Cell]]  # rows of cells, top to bottom


def pixels_per_cell(encoding: Encoding) -> tuple[int, int]:
    """(px wide, px tall) one cell holds: half (1, 2), quadrant (2, 2), braille (2, 4)."""
    raise NotImplementedError


def to_cells(img: Image.Image, encoding: Encoding = "half", *, background: RGB | None = None,
             foreground: RGB | None = None) -> CellGrid:
    """Dispatch to the encoder below. The image size should be an exact multiple of
    pixels_per_cell(encoding). Pad with `background` if not (decide: pad or crop?)."""
    raise NotImplementedError


def to_cells_half(img: Image.Image, *, background: RGB | None = None) -> CellGrid:
    """Pack pixel rows (0,1), (2,3), ... into half-block Cells: '▀' fg=top, bg=bottom.

    Edge cases: odd height (use `background` for the missing bottom pixel);
    top == bottom (a space with bg, or '█' with fg: same look, different cost).
    Done when: W x H px -> ceil(H/2) rows of W cells.
    """
    raise NotImplementedError


def to_cells_quadrant(img: Image.Image, *, background: RGB, foreground: RGB) -> CellGrid:
    """2x2 pixels -> one quadrant glyph. A pixel is "on" if it != background.

    Build a 16-entry lookup table indexed by a 4-bit mask, with your own bit order,
    e.g. upper-left=1, upper-right=2, lower-left=4, lower-right=8.
    mask 0 -> ' ', mask 15 -> '█', upper-left only -> '▘'. Fill in the other 13 from
    the Unicode Block Elements chart. Cell fg=foreground, bg=background.
    """
    raise NotImplementedError


def to_cells_braille(img: Image.Image, *, background: RGB, foreground: RGB) -> CellGrid:
    """2x4 pixels -> one braille glyph: chr(BRAILLE_BASE + mask).

    Unicode's dot numbering is NOT row-major. Bits by (x, y) inside the cell:
        (0,0)=0x01  (1,0)=0x08
        (0,1)=0x02  (1,1)=0x10
        (0,2)=0x04  (1,2)=0x20
        (0,3)=0x40  (1,3)=0x80
    (dots 7 and 8 were added to braille later, hence the odd bottom row).
    All 8 on -> '⣿' (U+28FF). Only top-left -> '⠁' (U+2801).
    """
    raise NotImplementedError


def cells_to_ansi(cells: CellGrid) -> str:
    """Debug helper: 24-bit ANSI escape codes, so you can print() the art without Textual.

    Foreground: ESC[38;2;R;G;Bm   Background: ESC[48;2;R;G;Bm   Reset: ESC[0m
    scripts/preview_art.py uses this.
    """
    raise NotImplementedError
