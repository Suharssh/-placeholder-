# linernotes

A black-and-white terminal app: type an artist's name, and their portrait appears
as 1-bit pixel art in the middle of your terminal.

**This repo is a scaffold.** Every function has a signature, a docstring, and
hints, and raises `NotImplementedError`. You write the bodies.

## Scope (this version)

1. A single search bar, centred on a black screen. It finds artists fuzzily as you type.
2. Choose an artist: the search bar moves to the top-left, and the artist's photo
   (you pick it) appears as black-and-white dithered pixel art in the middle of the
   screen, with equal padding on every side and resizing with the terminal.
3. Search again from the top-left bar to swap artists. Esc clears back to the centred bar.

That's it. Anything else (songs, graphs, recommendations) comes later.

## Setup (Windows, PowerShell)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -rs          # every test starts as SKIPPED ("not implemented yet")
```

Use **Windows Terminal** (not the old console window): it handles 24-bit colour
and the block/braille glyphs this project draws with. Cascadia Mono renders them
cleanly with no gaps between rows.

Live-reload while working on the UI: the Textual devtools (`textual console` in one
terminal, `textual run --dev ...` in another). See the devtools page in
[docs/RESOURCES.md](docs/RESOURCES.md).

## How to work through it

1. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): layers, data flow, and the
   decisions you'll make.
2. Follow [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) milestone by milestone.
   Each one says what to read, what to build, and which tests go green.
3. Record each decision in `docs/adr/` using the template. Write the ADR **before**
   the code, then update it with what you learned.
4. Portraits: [docs/PIXEL_ART.md](docs/PIXEL_ART.md) (1-bit dithering, glyph encodings).

## Repo map

```
data/catalog.json          sample artists (extend it)
palettes/mine.toml         black + white (optional dim grey for UI, your call)
assets/artists/            your chosen artist images (git-ignored)
scripts/preview_art.py     art pipeline in the terminal without Textual: fast tuning loop
src/linernotes/
  domain/                  Artist dataclass
  catalog/                 Catalog protocol + JSON adapter
  search/                  normalize -> fuzzy -> index
  art/                     palette, colorspace, pixelate, render, cache, pipeline
  ui/                      Textual app, MainScreen, widgets, layout math, TCSS
tests/                     contracts for each module (skipped until implemented)
docs/                      architecture, learning path, pixel art, resources, ADRs
```
