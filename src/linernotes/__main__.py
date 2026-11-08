"""Entry point: `python -m linernotes` or the `linernotes` console script."""

from __future__ import annotations

import argparse


def build_arg_parser() -> argparse.ArgumentParser:
    """Define the CLI flags.

    Suggested flags (you choose which ones to support):
        --catalog PATH     JSON catalog to load (default: data/catalog.json)
        --palette NAME     palette file in palettes/ to use (default: from settings)
        --dither MODE      none | ordered | floyd-steinberg
        --no-cache         re-render art on every launch

    Done when: `python -m linernotes --help` lists your flags.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Parse args, build Settings, construct LinerNotesApp, run it.

    Hints:
      * Keep this function thin: parse, wire, run. No logic belongs here.
      * Build Settings with `linernotes.config.load_settings(...)`.
      * `LinerNotesApp(settings).run()` blocks until the user quits.
      * Return an exit code (0 for success) so the console script behaves.
    """
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
