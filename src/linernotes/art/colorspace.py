"""Colour and brightness.

With a black-and-white palette, "which palette colour is nearest?" reduces to
"is this pixel brighter than some threshold?". So the function that matters most
is `luminance`: how bright a colour LOOKS. (R + G + B) / 3 is wrong. Pure green
looks far brighter than pure blue. Compare Rec. 709 luma and OKLab L on the same
portrait. Skin tones and coloured backgrounds come out visibly different.

DECISION D7: `nearest` (RGB vs OKLab) only matters if you ever use a palette
with more than two colours. Implement it anyway: it is the general case, and
the tests cover it.
"""

from __future__ import annotations

from collections.abc import Sequence

RGB = tuple[int, int, int]
Lab = tuple[float, float, float]


def srgb_to_linear(channel: int) -> float:
    """0..255 sRGB channel -> 0..1 linear light. (Gamma curve; see the OKLab post.)"""
    raise NotImplementedError


def rgb_to_oklab(rgb: RGB) -> Lab:
    """sRGB -> OKLab. Björn Ottosson's post gives the two 3x3 matrices and a cube root."""
    raise NotImplementedError


def luminance(rgb: RGB) -> float:
    """Perceived brightness in [0, 1]. 0 = black, 1 = white.

    Options: Rec. 709 relative luminance on LINEAR channels
    (0.2126 R + 0.7152 G + 0.0722 B), or OKLab L. Pick one, write down why.
    Either way: pure green must come out brighter than pure blue.
    """
    raise NotImplementedError


def distance_rgb(a: RGB, b: RGB) -> float:
    """Squared Euclidean distance in RGB. (Why squared? You only compare, never display.)"""
    raise NotImplementedError


def distance_oklab(a: Lab, b: Lab) -> float:
    """Squared Euclidean distance in OKLab."""
    raise NotImplementedError


def nearest(rgb: RGB, palette: Sequence[RGB], *, space: str = "oklab") -> RGB:
    """Return the palette colour closest to `rgb`.

    Performance: this runs once per pixel (e.g. 160x100 = 16,000 times per render).
    Convert the palette to OKLab ONCE, not once per pixel. Later options to look
    up: functools.lru_cache on the input colour, or a 32x32x32 lookup table.
    """
    raise NotImplementedError
