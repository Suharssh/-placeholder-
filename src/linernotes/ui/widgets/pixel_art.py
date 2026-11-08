"""Draws a CellGrid (from art/render.py) using Textual's Line API.

Why the Line API (render_line) rather than render() returning a big Text?
Textual asks for one line at a time and caches the result as a Strip, so the art
doesn't get rebuilt into one giant Text on every refresh. Read
"Line API" in the Textual widgets guide.
"""

from __future__ import annotations

from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget

from linernotes.art.render import Cell, CellGrid


class PixelArt(Widget):
    # Setting this triggers a refresh. layout=True also re-measures the widget size.
    cells: reactive[CellGrid | None] = reactive(None, layout=True)

    def get_content_width(self, container, viewport) -> int:  # noqa: ANN001
        """Width in cells = len(row). Lets CSS `width: auto` size the widget to the art."""
        raise NotImplementedError

    def get_content_height(self, container, viewport, width) -> int:  # noqa: ANN001
        """Height in cells = number of rows."""
        raise NotImplementedError

    def render_line(self, y: int) -> Strip:
        """Return row `y` as a Strip of rich Segments.

        Each Cell becomes Segment(cell.char, Style(color=..., bgcolor=...)).
        Out-of-range y -> Strip.blank(self.size.width).
        Performance: build each row's Strip ONCE when `cells` changes (watch_cells),
        store them, and just index here. Combining runs of identical cells
        into one Segment cuts output size a lot. Measure the difference.
        """
        raise NotImplementedError

    def watch_cells(self, cells: CellGrid | None) -> None:
        """Called when `cells` changes: pre-build and store the row Strips."""
        raise NotImplementedError


def cell_to_segment(cell: Cell):  # -> rich.segment.Segment
    """Cell -> rich Segment. Cache rich Style objects: with a 2-colour palette there
    are at most 4 fg/bg combinations in the whole image."""
    raise NotImplementedError
