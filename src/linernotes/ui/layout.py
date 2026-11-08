"""Layout math as pure functions, so the "equal padding" requirement can be unit-tested.

Textual's CSS (`align: center middle`) centres a widget for you. But the widget's
SIZE must be computed: as large as possible, aspect ratio preserved, with at least
`margin` cells on every side. That's this function. The CSS centres the result.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Box:
    x: int      # left padding in cells
    y: int      # top padding in cells
    cols: int   # art width in cells
    rows: int   # art height in cells

    # Note: no pixel size here. The box is about PHYSICAL space on screen. How many
    # pixels fit inside depends on the glyph encoding (half/quadrant/braille);
    # that's art.pipeline.pixel_size_for_box's job. Keep the two concerns apart.


def compute_art_box(
    term_cols: int,
    term_rows: int,
    image_aspect: float,
    *,
    margin: int = 2,
    reserved_rows: int = 0,
) -> Box:
    """Largest centred box for an image of physical aspect `image_aspect` (= width / height).

    Steps:
      1. Usable area = terminal minus `margin` on all sides, minus `reserved_rows`
         (the search input, footer...).
      2. Convert to a CELL aspect. A cell is about twice as tall as wide, so a box of
         C x R cells has physical aspect C / (2R). Solve for C/R. This holds for
         EVERY glyph encoding. Convince yourself why.
      3. Fit: try full usable width and compute the height; if too tall, fit by height.
      4. Centre: leftover space split evenly. With an odd leftover, which side gets
         the extra cell? Decide and be consistent.
    Never return cols or rows < 1. A tiny terminal still needs a valid box.

    tests/test_layout.py states the contract.
    """
    raise NotImplementedError
