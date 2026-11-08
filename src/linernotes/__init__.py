"""linernotes: search for an artist, see them as black-and-white pixel art in your terminal.

Package layout (read docs/ARCHITECTURE.md before writing code):

    domain/   plain dataclasses (Artist). Imports nothing from this package.
    catalog/  where Artists come from (a local JSON file).
    search/   the search engine: normalize, fuzzy scoring, index, ranking.
    art/      image -> 1-bit pixel grid -> terminal cells.
    ui/       Textual app, screens, widgets, TCSS. The only layer that imports Textual.

Dependency rule: ui -> (search, art, catalog) -> domain. Never the other way.
"""

__version__ = "0.1.0"
