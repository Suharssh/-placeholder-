# Resources

Grouped by milestone. Read **the bolded ones**; the rest are for when you're curious or stuck.

## Architecture and decision-making (M0, throughout)
* **Michael Nygard, "Documenting Architecture Decisions"** (the original ADR post): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
* ADR community site, templates and examples: https://adr.github.io/
* **Alistair Cockburn, Hexagonal Architecture (ports and adapters)**: https://alistair.cockburn.us/hexagonal-architecture/
* **Architecture Patterns with Python** (free online book; the repository/ports chapters map directly onto `catalog/`): https://www.cosmicpython.com/
* Python `typing.Protocol` (structural typing for the Catalog port): https://docs.python.org/3/library/typing.html#typing.Protocol

## Textual and Rich (M0, M5, M7, M8)
* **Textual tutorial**: https://textual.textualize.io/tutorial/
* **Textual guide** (App, Screens, Events, CSS, Widgets, Workers, Testing): https://textual.textualize.io/guide/
  * Screens: https://textual.textualize.io/guide/screens/
  * Events and messages: https://textual.textualize.io/guide/events/
  * **Reactivity** (`reactive`, `watch_*`, used for MainScreen's state): https://textual.textualize.io/guide/reactivity/
  * **CSS** (selectors, classes like `.-showing`): https://textual.textualize.io/guide/CSS/
  * Layout (dock, layers): https://textual.textualize.io/guide/layout/
  * Animation (stretch: animate the search bar's move): https://textual.textualize.io/guide/animation/
  * Widgets, including the **Line API** used by `PixelArt`: https://textual.textualize.io/guide/widgets/
  * **Workers** (thread workers, `exclusive`, `call_from_thread`): https://textual.textualize.io/guide/workers/
  * Devtools (`textual console`, `textual run --dev`): https://textual.textualize.io/guide/devtools/
  * Testing with `run_test()` / Pilot: https://textual.textualize.io/guide/testing/
* Widget reference, Input: https://textual.textualize.io/widgets/input/ · OptionList: https://textual.textualize.io/widgets/option_list/
* Styles used by the two states: `align` https://textual.textualize.io/styles/align/ · `dock` https://textual.textualize.io/styles/dock/ · `layers` https://textual.textualize.io/styles/layers/ · `display` https://textual.textualize.io/styles/display/
* Textual source code, worth reading when the docs run out: https://github.com/Textualize/textual
* Rich docs (Segment, Style, Text): https://rich.readthedocs.io/

## Search (M1-M4)
* Python `unicodedata`: https://docs.python.org/3/library/unicodedata.html
* **Levenshtein distance**: https://en.wikipedia.org/wiki/Levenshtein_distance
* Damerau-Levenshtein (transpositions): https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
* Trie: https://en.wikipedia.org/wiki/Trie · BK-tree: https://en.wikipedia.org/wiki/BK-tree
* RapidFuzz (compare against your own implementation): https://github.com/rapidfuzz/RapidFuzz
* Python `timeit`: https://docs.python.org/3/library/timeit.html

## 1-bit pixel art (M6)
* **Tanner Helland, "Image Dithering: Eleven Algorithms and Source Code"** (Floyd-Steinberg, Atkinson, and others, explained side by side): https://tannerhelland.com/2012/12/28/dithering-eleven-algorithms-source-code.html
* **Ordered dithering (Bayer matrix)**: https://en.wikipedia.org/wiki/Ordered_dithering
* Floyd-Steinberg dithering: https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
* Relative luminance (Rec. 709 weights, linear vs gamma-encoded): https://en.wikipedia.org/wiki/Relative_luminance
* Björn Ottosson, OKLab (perceptual lightness L; colour distance if you go beyond 2 colours): https://bottosson.github.io/posts/oklab/
* Unicode Block Elements (`▀ ▄ █` and quadrants `▘▝▖▗▚▞`): https://en.wikipedia.org/wiki/Block_Elements
* **Unicode Braille Patterns** (the dot-bit layout used by `to_cells_braille`): https://en.wikipedia.org/wiki/Braille_Patterns
* Pillow docs (`Image.resize` filters, `ImageEnhance`, `ImageOps.exif_transpose`): https://pillow.readthedocs.io/
* Pedro Medeiros (Saint11) pixel art tutorials (short and visual; the light/shading ones apply to 1-bit too): https://studiominiboss.itch.io/pixel-art-tutorials
* rich-pixels (Darren Burns): a small library that does half-block rendering. **Read it after you've written your own `render.py`**, not before: https://github.com/darrenburns/rich-pixels
* Editors for hand-cleaning portraits: Aseprite https://www.aseprite.org/ · Pixelorama (free) https://orama-interactive.itch.io/pixelorama

## Terminal (Windows)
* Windows Terminal docs: https://learn.microsoft.com/en-us/windows/terminal/
* ANSI escape codes, 24-bit colour section: https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit

