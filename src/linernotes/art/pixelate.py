"""Image -> small, palette-limited pixel grid (a Pillow Image in mode "RGB").

With the black-and-white palette, this module decides how a photo of a face
becomes a pattern of black and white pixels. Dithering is the core of it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from PIL import Image

from linernotes.art.palette import Palette

DitherMode = Literal["none", "ordered", "atkinson", "floyd-steinberg"]


def load_image(path: Path) -> Image.Image:
    """Open, apply EXIF orientation (ImageOps.exif_transpose), convert to RGB.

    Phone photos are often stored sideways and rotated by an EXIF flag. Skip
    this step and some portraits will render lying down.
    """
    raise NotImplementedError


def crop_to_aspect(img: Image.Image, aspect: float, *, focus: tuple[float, float] = (0.5, 0.4)) -> Image.Image:
    """Crop (never stretch) to width/height == aspect.

    `focus` is where to keep, as fractions of (width, height). For portraits the
    face is usually above centre, hence 0.4.
    """
    raise NotImplementedError


def to_grayscale(img: Image.Image) -> Image.Image:
    """RGB -> mode "L" (0..255) using YOUR luminance choice (colorspace.luminance).

    Pillow's img.convert("L") uses a fixed formula on gamma-encoded values.
    Compare it with yours on a colourful photo.
    """
    raise NotImplementedError


def preprocess(img: Image.Image, *, contrast: float = 1.4, brightness: float = 1.0, gamma: float = 1.0) -> Image.Image:
    """Shape the tones BEFORE shrinking and dithering. This matters most in 1-bit.

    A dithered face only reads if it has a few clear tonal zones:
    deep shadows, mid-tones, highlights. Boost contrast (ImageEnhance.Contrast),
    and try a gamma curve to pull detail out of dark skin or dark backgrounds.
    Stretch: CLAHE / local contrast ("autocontrast" per region).
    These numbers are taste. Expose them in Settings once you have a feel for them.
    """
    raise NotImplementedError


def downscale(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize to exactly `size` (width, height) pixels.

    Filters: NEAREST (noisy), BOX (clean average), LANCZOS (sharp, can halo).
    For dithering, a slightly SHARP downscale (LANCZOS) often reads better:
    dithering softens edges, so you want them crisp going in. Compare. (D8a)

    Note: `size` need not have the image's aspect ratio. For quadrant
    encoding the pixel grid is deliberately squashed (render.pixels_per_cell).
    """
    raise NotImplementedError


def bayer_matrix(n: int) -> list[list[float]]:
    """n x n ordered-dither threshold matrix (n a power of 2), values in [0, 1).

    Build it recursively from the 2x2 base (Wikipedia "Ordered dithering").
    """
    raise NotImplementedError


def quantize(img: Image.Image, palette: Palette, *, dither: DitherMode = "atkinson", strength: float = 1.0) -> Image.Image:
    """Map every pixel to a palette colour.

    DECISION D8b, dithering. With 2 colours this choice IS the look:
      none            -> hard threshold. Bold, poster-like silhouettes. Faces lose detail.
      ordered (Bayer) -> regular cross-hatch texture. Each pixel decided
                         independently, so stable if you ever animate it.
      atkinson        -> classic 1-bit Macintosh look. Spreads only 6/8 of the
                         error, so highlights and shadows stay clean and contrasty.
                         Usually the best-looking for 1-bit portraits.
      floyd-steinberg -> spreads all the error. Smoothest greys, but muddier and
                         "noisier" than Atkinson in 1-bit.
    Error-diffusion methods (atkinson, floyd-steinberg) ripple when one input
    pixel changes, so they flicker in animation. Ordered dithering doesn't.

    1-bit fast path (palette.is_one_bit): work in grayscale, compare against a
    threshold, output palette.background / palette.foreground. No colour search.

    Done when: every pixel of the result is in palette.colors (there's a test).
    """
    raise NotImplementedError


def pixelate(
    img: Image.Image,
    palette: Palette,
    size: tuple[int, int],
    *,
    dither: DitherMode = "atkinson",
) -> Image.Image:
    """crop_to_aspect -> preprocess -> downscale -> quantize. Just composition."""
    raise NotImplementedError
