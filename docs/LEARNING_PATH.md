# Learning path

Each milestone: **Read** → **Decide** (write the ADR) → **Build** → **Done when**.
Run `pytest -rs` constantly. Skips turning into passes is your progress bar.
Commit at the end of every milestone.

---

### M0: Setup and orientation (½ day)
* **Read:** README, ARCHITECTURE §1-2. Textual tutorial (the stopwatch app) end to end.
* **Decide:** D1 (language/framework). Write `docs/adr/0001-tui-framework.md`.
* **Build:** venv, `pip install -e ".[dev]"`, `pytest -rs` shows all skipped.
  Run `python -m textual` to see the demo in your terminal.
* **Done when:** you can explain the dependency rule in one sentence, and the
  Textual tutorial app runs in Windows Terminal.

### M1: Text normalization (½ day)
* **Read:** Python `unicodedata` docs (NFKD, `combining`), `str.casefold`.
* **Build:** `search/normalize.py`.
* **Done when:** `tests/test_normalize.py` passes.

### M2: Fuzzy scoring (1 day)
* **Read:** Levenshtein distance (Wikipedia, DP section). Optional: how RapidFuzz's
  `ratio` / `partial_ratio` / `token_sort_ratio` differ.
* **Decide:** D6 draft. Write your 10-query table first.
* **Build:** `levenshtein` (full table → two rows), `similarity`, `prefix_score`, `score`.
* **Done when:** `tests/test_fuzzy.py` passes and you can state levenshtein's time and space complexity.

### M3: Catalog (½ day)
* **Read:** "ports and adapters" (Cockburn); `typing.Protocol`.
* **Build:** `catalog/json_catalog.py` with validation.
* **Done when:** `tests/test_catalog.py` passes.

### M4: Search index (1 day)
* **Decide:** D5. Implement option (a). `timeit` it on 10k generated names, and record the number in the ADR.
* **Build:** `search/index.py` (`search`; leave `highlight_spans` returning `()` for now).
* **Done when:** `tests/test_index.py` passes; per-keystroke search time recorded.

### M5: Search UI, state 1 (1-2 days)
* **Read:** Textual guide: App basics, Screens, Events and messages, Reactivity, CSS;
  widget docs for `Input` and `OptionList`.
* **Decide:** D3.
* **Build:** `config.py`, `__main__.py`, `ui/app.py`, `SearchBox`, `MainScreen`
  (compose, on_mount, on_search_box_selected; `watch_artist` can just `notify` the name for now),
  TCSS for state 1.
* **Done when:** `python -m linernotes` opens a black screen with a centred search bar;
  typing filters artists live; arrows + Enter select; Ctrl+Q quits.
* **Stretch:** `highlight_spans` + bold matched characters.

### M6: Art pipeline, outside the UI (2-3 days)
* **Read:** PIXEL_ART.md fully; Tanner Helland's dithering article (error diffusion,
  Atkinson); "Ordered dithering" (Wikipedia); Rec. 709 luminance; Unicode Block Elements
  and Braille Patterns charts.
* **Decide:** D2 (encoding), D7 (luminance), D8 (dither + tone), D9 (strict 1-bit?).
* **Build:** `art/palette.py`, `colorspace.py`, `pixelate.py` (implement all four
  dithers, since comparing them is the lesson), `render.py` (all three encodings),
  `pipeline.py`, `scripts/preview_art.py`.
* **Done when:** `tests/test_palette.py` + `tests/test_art.py` pass, and
  `preview_art.py --compare-dither` / `--compare-encoding` on 3 different portraits
  convinced you of your defaults. Screenshots go in the ADRs.

### M7: State 2: bar to the top-left, art in the middle (2 days)
* **Read:** Textual guide: Widgets → Line API; Workers; styles `align`, `dock`, `layers`, `display`.
* **Decide:** D4, D11.
* **Build:** `ui/layout.py`, `PixelArt` widget, `MainScreen.watch_artist` / `request_render` /
  `on_resize` / `action_clear`, TCSS for state 2.
* **Done when:** `tests/test_layout.py` passes; choosing an artist moves the bar to the
  top-left and shows the portrait centred with equal padding; searching again swaps the
  art; Esc returns to the centred bar; dragging the window edge re-renders without freezing.

### M8: UI test (½ day)
* **Decide:** D12.
* **Build:** one `Pilot` test: type "kend" → Enter → assert `-showing` is set and
  `PixelArt` is displayed → Esc → assert it's gone.
* **Done when:** that test passes.

---

### Exit checklist
- [ ] All tests pass; remove the NotImplementedError → skip hook from `tests/conftest.py`.
- [ ] ADRs exist for D1-D9 and D11 (D10, D12 at least drafted).
- [ ] `grep` shows no Textual imports in `search/` or `art/`.
- [ ] Your own images, 5+ artists in the catalog, everything black and white (or your D9 grey).
- [ ] A screen recording of search → portrait → search again (Windows: Win+Alt+R).
