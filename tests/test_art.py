import pytest
from PIL import Image

from linernotes.art.palette import Palette
from linernotes.art.pipeline import pixel_size_for_box
from linernotes.art.pixelate import bayer_matrix, crop_to_aspect, downscale, quantize, to_grayscale
from linernotes.art.render import (
    pixels_per_cell,
    to_cells_braille,
    to_cells_half,
    to_cells_quadrant,
)

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
MONO = Palette(name="mono", colors=(BLACK, WHITE), explicit_background=BLACK)
FOUR = Palette(name="t", colors=((0, 0, 0), (128, 0, 128), (255, 200, 0), (255, 255, 255)))
DITHERS = ["none", "ordered", "atkinson", "floyd-steinberg"]


def gradient(w=64, h=48) -> Image.Image:
    img = Image.new("RGB", (w, h))
    img.putdata([(x * 4 % 256, y * 5 % 256, 128) for y in range(h) for x in range(w)])
    return img


def colors_in(img):
    return {c for _, c in img.getcolors(maxcolors=img.width * img.height)}


def mono_image(w, h, on):
    """w x h black image with the given (x, y) pixels white."""
    img = Image.new("RGB", (w, h), BLACK)
    for p in on:
        img.putpixel(p, WHITE)
    return img


# ---- pixelate --------------------------------------------------------------

def test_crop_to_aspect():
    out = crop_to_aspect(gradient(100, 50), 1.0)
    assert out.size[0] == out.size[1] == 50


def test_downscale_exact_size():
    assert downscale(gradient(), (16, 12)).size == (16, 12)


def test_grayscale_mode():
    assert to_grayscale(gradient()).mode == "L"


def test_bayer():
    m = bayer_matrix(4)
    flat = sorted(v for row in m for v in row)
    assert len(flat) == 16 and len(set(flat)) == 16
    assert 0.0 <= flat[0] and flat[-1] < 1.0


@pytest.mark.parametrize("dither", DITHERS)
@pytest.mark.parametrize("palette", [MONO, FOUR], ids=["mono", "four"])
def test_quantize_only_palette_colors(dither, palette):
    assert colors_in(quantize(gradient(), palette, dither=dither)) <= set(palette.colors)


@pytest.mark.parametrize("dither", ["ordered", "atkinson", "floyd-steinberg"])
def test_dither_makes_mid_grey_a_mix(dither):
    # The whole point of dithering in 1-bit: a flat 50% grey becomes roughly half white pixels.
    grey = Image.new("RGB", (32, 32), (128, 128, 128))
    out = quantize(grey, MONO, dither=dither)
    counts = {color: n for n, color in out.getcolors(maxcolors=32 * 32)}
    frac = counts.get(WHITE, 0) / (32 * 32)
    assert 0.25 < frac < 0.75, f"{dither}: {frac:.2f} white"


def test_ordered_is_frame_stable():
    a = quantize(gradient(), MONO, dither="ordered")
    b = quantize(gradient(), MONO, dither="ordered")
    assert a.tobytes() == b.tobytes()


# ---- encodings -------------------------------------------------------------

@pytest.mark.parametrize("enc, ppc", [("half", (1, 2)), ("quadrant", (2, 2)), ("braille", (2, 4))])
def test_pixels_per_cell(enc, ppc):
    assert pixels_per_cell(enc) == ppc


def test_pixel_size_for_box():
    assert pixel_size_for_box(40, 20, "half") == (40, 40)
    assert pixel_size_for_box(40, 20, "braille") == (80, 80)


def test_half_shape_and_odd_height():
    assert [len(r) for r in to_cells_half(Image.new("RGB", (7, 10)))] == [7] * 5
    assert len(to_cells_half(Image.new("RGB", (3, 5)), background=BLACK)) == 3


def test_half_block_colors():
    img = mono_image(1, 2, [(0, 0)])  # top white, bottom black
    (cell,), = to_cells_half(img)
    if cell.char == "▀":
        assert (cell.fg, cell.bg) == (WHITE, BLACK)
    elif cell.char == "▄":
        assert (cell.fg, cell.bg) == (BLACK, WHITE)
    else:
        pytest.fail(f"unexpected glyph {cell.char!r}")


@pytest.mark.parametrize(
    "on, glyph",
    [([], " "), ([(0, 0), (1, 0), (0, 1), (1, 1)], "█"), ([(0, 0)], "▘"), ([(1, 1)], "▗"),
     ([(0, 0), (1, 0)], "▀"), ([(0, 0), (1, 1)], "▚")],
)
def test_quadrant(on, glyph):
    (cell,), = to_cells_quadrant(mono_image(2, 2, on), background=BLACK, foreground=WHITE)
    assert cell.char == glyph


@pytest.mark.parametrize(
    "on, glyph",
    [([], "⠀"), ([(0, 0)], "⠁"), ([(1, 0)], "⠈"), ([(0, 3)], "⡀"), ([(1, 3)], "⢀"),
     ([(x, y) for x in range(2) for y in range(4)], "⣿")],
)
def test_braille(on, glyph):
    (cell,), = to_cells_braille(mono_image(2, 4, on), background=BLACK, foreground=WHITE)
    assert cell.char == glyph


def test_braille_shape():
    cells = to_cells_braille(Image.new("RGB", (10, 12)), background=BLACK, foreground=WHITE)
    assert len(cells) == 3 and all(len(r) == 5 for r in cells)
