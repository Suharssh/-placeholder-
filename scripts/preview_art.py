"""Fast feedback loop for the art pipeline, without Textual.

    python scripts/preview_art.py assets/artists/kendrick-lamar.png --palette mine --cols 80
    python scripts/preview_art.py <img> --compare-dither     # none | ordered | atkinson | floyd-steinberg
    python scripts/preview_art.py <img> --compare-encoding   # half | quadrant | braille, same box size
    python scripts/preview_art.py <img> --compare-luma       # Pillow convert("L") vs your luminance()

You will tune the art 100x more often than you change the UI. Make this loop fast.
Use Windows Terminal: it supports 24-bit colour; the old console may not.
"""

from __future__ import annotations

import argparse


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    raise NotImplementedError


def side_by_side(blocks: list[str], gap: int = 2) -> str:
    """Join several multi-line ANSI strings horizontally, for comparisons.

    Careful: ANSI escape codes have zero display width, so len(line) is wrong
    for padding. Pad using the known cell width instead.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """load_settings -> load_palette -> render_art -> cells_to_ansi -> print."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
