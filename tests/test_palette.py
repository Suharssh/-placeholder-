import pytest

from linernotes.art.colorspace import luminance, nearest, rgb_to_oklab
from linernotes.art.palette import load_palette, parse_hex, to_hex


@pytest.mark.parametrize("s, rgb", [("#ff8800", (255, 136, 0)), ("ff8800", (255, 136, 0)), ("#f80", (255, 136, 0))])
def test_parse_hex(s, rgb):
    assert parse_hex(s) == rgb


@pytest.mark.parametrize("bad", ["", "#12", "#gggggg", "12345"])
def test_parse_hex_rejects(bad):
    with pytest.raises(ValueError):
        parse_hex(bad)


def test_roundtrip():
    assert to_hex(parse_hex("#1a2b3c")) == "#1a2b3c"


def test_load_palette(palette_path):
    pal = load_palette(palette_path)
    assert len(pal.colors) >= 2
    assert len(set(pal.colors)) == len(pal.colors)


def test_mono_palette(palette_path):
    pal = load_palette(palette_path)
    assert pal.is_one_bit
    assert pal.background == (0, 0, 0)
    assert pal.foreground == (255, 255, 255)


def test_luminance():
    assert luminance((0, 0, 0)) < 1e-6
    assert abs(luminance((255, 255, 255)) - 1.0) < 1e-3
    assert luminance((0, 255, 0)) > luminance((255, 0, 0)) > luminance((0, 0, 255))


def test_oklab_white_and_black():
    L_white, a, b = rgb_to_oklab((255, 255, 255))
    assert abs(L_white - 1.0) < 1e-3 and abs(a) < 1e-3 and abs(b) < 1e-3
    assert abs(rgb_to_oklab((0, 0, 0))[0]) < 1e-6


@pytest.mark.parametrize("space", ["rgb", "oklab"])
def test_nearest_exact(space):
    pal = [(0, 0, 0), (255, 0, 0), (255, 255, 255)]
    assert nearest((255, 0, 0), pal, space=space) == (255, 0, 0)
    assert nearest((250, 10, 5), pal, space=space) == (255, 0, 0)
