# Architecture

This document describes the shape of the system and lists the decisions you
need to make. It deliberately does **not** answer most of them. Each decision
has the question, the realistic options, what to weigh, and what to read. Your
answer goes in an ADR (`docs/adr/`).

## 1. Layers and the dependency rule

```
┌────────────────────────────────────────────────────────────┐
│ ui/        Textual: App, MainScreen, SearchBox, PixelArt,   │  imports everything below
│            TCSS, layout                                     │
├───────────────────────┬────────────────────────────────────┤
│ search/               │ art/                               │  pure logic, no Textual
│ normalize, fuzzy,     │ palette, colorspace, pixelate,     │  (art uses Pillow)
│ index                 │ render, cache, pipeline            │
├───────────────────────┴────────────────────────────────────┤
│ catalog/   Catalog protocol (port) + JsonCatalog (adapter)  │
├────────────────────────────────────────────────────────────┤
│ domain/    Artist                                           │  imports nothing
└────────────────────────────────────────────────────────────┘
```

**Rule:** arrows point down only. `search/` and `art/` never import `textual`.

Why this matters:
* Everything below `ui/` is unit-testable with plain pytest, with no terminal.
* Swapping the data source (`catalog/`) later doesn't touch the UI.
* You can tune the art 100x faster with `scripts/preview_art.py` than by
  relaunching the app.

Check yourself: `grep -r "import textual\|from textual" src/linernotes/search src/linernotes/art` should print nothing.

**Visual direction:** black background, white everything, no colour (palette =
`#000000` + `#ffffff`). Hierarchy comes from bold/reverse text, case, and space.

## 2. Data flow, step by step

**Startup**
`__main__.main` → `load_settings` → `LinerNotesApp(settings)` → `on_mount`:
load `JsonCatalog`, load `Palette`, build `SearchIndex[Artist]`, push `MainScreen(index)`.
State 1: search bar centred, art hidden.

**Typing** (every keystroke)
`Input.Changed` → `SearchBox.on_input_changed` → `index.search(q)` →
`normalize` → `_candidates` → `fuzzy.score` each → sort, dedupe, limit → `OptionList` updated.
Runs synchronously on the event loop, so it must stay fast (target: under 5 ms).

**Choosing an artist**
`Enter` → `SearchBox.Selected(artist)` bubbles → `MainScreen.on_search_box_selected`
→ `self.artist = artist` → `watch_artist`:
1. `set_class(True, "-showing")` → TCSS moves the search bar to the top-left and shows `PixelArt`;
2. `request_render()` → `layout.compute_art_box(...)` → `Box` → worker thread:
   `pipeline.render_art(image, palette, box.cols, box.rows)` → `CellGrid` →
   back on the UI thread: `PixelArt.cells = grid` → `render_line` per row.

**Searching again** (state 2)
Same flow. The dropdown draws on a layer above the art. Choosing swaps `self.artist`,
so `watch_artist` re-renders.

**Esc**
`action_clear` → `self.artist = None` → `watch_artist` removes `-showing` → bar back to centre, art hidden.

**Resize**
`on_resize` → debounce → `request_render()` at the new size (exclusive worker cancels a stale one).

## 3. Decisions

Each one becomes `docs/adr/NNNN-title.md`. Do them roughly in this order.

### D1: Language and TUI framework
The scaffold uses **Python + Textual**. Do not take that on faith; justify it or replace it.
* Options: Python/Textual · Rust/ratatui · Go/Bubble Tea · TypeScript/Ink · raw curses.
* Weigh: your fluency, whether there is a layout engine (centring, docking, layers,
  resizing) or you write it yourself, async story, image libraries, Windows support.
* Exercise: build "a box that's centred, then moves to the top-left on Enter" in
  Textual, and read how you'd do it in ratatui. The difference in effort is the argument.

### D2: How pixels become terminal characters
See `art/render.py` and PIXEL_ART.md.
* Options: half blocks `▀` (1×2 px/cell, chunky) · quadrant `▚` (2×2, tall pixels) ·
  braille `⣿` (2×4 dots) · ASCII density ramp · graphics protocols (Sixel, Kitty).
* With a black-and-white palette, the "2 colours per cell" limit of quadrant and
  braille costs nothing, so this is purely resolution vs look: chunky pixel art
  (half) vs fine dot-matrix (braille).
* Weigh: how faces read at your typical box size, font rendering on Windows Terminal.

### D3: Screens and state
One screen with two states (CSS class `-showing`) vs two screens (push/pop).
The requirement (the same search bar moves from centre to top-left) points to one
screen. Write down *why* in your own words. Also: services on `App` reached via
`self.app` vs passed into the Screen constructor. Which is easier to test with a fake?

### D4: Where and when art is rendered
* Synchronously in the event handler (simple, freezes the UI) vs a **thread worker**
  (`@work(thread=True, exclusive=True)`) vs pre-rendering at startup.
* Debounce resize events? Cache by `(image, palette, size, dither, encoding)`? Memory or disk?
* Weigh: measured render time (time it), smoothness while resizing,
  stale results arriving after a newer request (exclusive workers).

### D5: Search data structure
`search/index.py` lists options (a)-(d). Weigh: dataset size (tens to thousands of
artists), keystroke latency budget, memory, code complexity, *learning goals*.
Measure (a) with `timeit` on 10,000 fake artist names before deciding you need (b)-(d).

### D6: Ranking
How prefix, token and edit-distance signals combine (`fuzzy.score`).
Make a table: 10 queries a real user would type (including typos and partial words)
× expected top result, and check each candidate formula against it. Keep the
table in the ADR. It doubles as a regression test (add it to `test_index.py`).

### D7: Brightness
In 1-bit, "nearest colour" is "brighter than a threshold?". Average of RGB vs
Rec. 709 luminance vs OKLab L (`colorspace.luminance`). Compare on a colourful photo
with `preview_art.py --compare-luma`.

### D8: Resampling, tone shaping, dithering
(a) downscale filter: BOX vs LANCZOS (dithering likes crisp input). (b) `preprocess`
contrast/gamma defaults. (c) dither: none / ordered / Atkinson / Floyd-Steinberg.
Keep screenshots of each in the ADR.

### D9: Strict 1-bit or one dim grey?
`palettes/mine.toml` has an optional `[ui] dim` colour for secondary text (e.g.
unhighlighted search results). Strict 1-bit uses bold/normal contrast only. How do
palette colours reach TCSS (comment at the top of `app.tcss`)?

### D10: Data source
Local JSON (now). When would it become SQLite or an API? Sync `Catalog` now;
would a network source force async later?

### D11: The search bar's move
Instant (class toggle only) vs animated (`styles.animate("offset", ...)`). How the
art avoids the corner bar: the bar lives inside an equal top margin
(margin = bar height + 1; there's a test for it) vs reserved rows vs letting the
art overlap under it. And what does the input contain after choosing an artist:
cleared, or the artist's name?

### D12: Testing the UI
Pure logic: pytest (done). UI: Textual's `App.run_test()` + `Pilot` to simulate
typing and keypresses. Assert the state, not pixels: after Enter, does the screen
have `-showing`? Is `PixelArt` displayed? Optionally snapshot tests
(`pytest-textual-snapshot`) for the two layouts.

## 4. Non-goals for this version

No songs, no graphs, no recommendations, no network calls. Search → portrait only.
