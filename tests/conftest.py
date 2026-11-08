"""Test harness.

Every test here is a CONTRACT for a function you haven't written yet. A test
that hits a NotImplementedError is reported as SKIPPED ("not implemented yet")
instead of failing. Run `pytest -rs` and watch the skips turn into passes as
you work through docs/LEARNING_PATH.md.

When everything is implemented, delete the hook below so a stray
NotImplementedError becomes a real failure again.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # noqa: ANN001
    outcome = yield
    report = outcome.get_result()
    if call.excinfo is not None and call.excinfo.errisinstance(NotImplementedError):
        report.outcome = "skipped"
        report.longrepr = (str(item.path), item.location[1] or 0, "not implemented yet")


@pytest.fixture
def catalog_path() -> Path:
    return ROOT / "data" / "catalog.json"


@pytest.fixture
def palette_path() -> Path:
    return ROOT / "palettes" / "mine.toml"
