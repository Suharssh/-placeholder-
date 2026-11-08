"""The 'art takes the middle of the screen, equal padding on all sides' requirement, as tests."""

import pytest

from linernotes.ui.layout import compute_art_box

SIZES = [(80, 24), (120, 40), (200, 55), (60, 50), (300, 30)]
ASPECTS = [1.0, 0.75, 16 / 9]


@pytest.mark.parametrize("cols, rows", SIZES)
@pytest.mark.parametrize("aspect", ASPECTS)
def test_fits_with_margin(cols, rows, aspect):
    b = compute_art_box(cols, rows, aspect, margin=2)
    assert b.x >= 2 and b.y >= 2
    assert b.x + b.cols <= cols - 2
    assert b.y + b.rows <= rows - 2


@pytest.mark.parametrize("cols, rows", SIZES)
@pytest.mark.parametrize("aspect", ASPECTS)
def test_centred(cols, rows, aspect):
    b = compute_art_box(cols, rows, aspect, margin=2)
    left, right = b.x, cols - (b.x + b.cols)
    top, bottom = b.y, rows - (b.y + b.rows)
    assert abs(left - right) <= 1
    assert abs(top - bottom) <= 1


@pytest.mark.parametrize("aspect", ASPECTS)
def test_aspect_preserved(aspect):
    b = compute_art_box(200, 60, aspect, margin=2)
    physical = b.cols / (2 * b.rows)  # cells are ~1:2
    assert abs(physical - aspect) / aspect < 0.06  # within rounding


def test_uses_space():
    # "As large as possible": one dimension should touch the margin.
    b = compute_art_box(120, 40, 1.0, margin=2)
    assert b.cols == 120 - 4 or b.rows == 40 - 4


def test_tiny_terminal_still_valid():
    b = compute_art_box(5, 3, 1.0, margin=2)
    assert b.cols >= 1 and b.rows >= 1


@pytest.mark.parametrize("cols, rows", SIZES)
def test_search_bar_fits_in_top_margin(cols, rows):
    # MainScreen rule: margin = search bar height + 1, so the top-left bar never overlaps the art
    # and padding stays equal on all four sides.
    bar_rows = 3
    b = compute_art_box(cols, rows, 1.0, margin=bar_rows + 1)
    assert b.y >= bar_rows + 1
    left, right = b.x, cols - (b.x + b.cols)
    top, bottom = b.y, rows - (b.y + b.rows)
    assert abs(left - right) <= 1 and abs(top - bottom) <= 1


def test_reserved_rows():
    b = compute_art_box(120, 40, 1.0, margin=2, reserved_rows=5)
    assert b.rows <= 40 - 4 - 5
