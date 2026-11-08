"""The Textual App: builds the shared services and shows MainScreen.

There's one screen (ui/screens/main.py). It switches between "search centred"
and "search top-left + art in the middle" with a CSS class, not by pushing screens.

Read the Textual guide pages on App basics, Screens, Reactivity and Workers
before filling this in (RESOURCES.md).
"""

from __future__ import annotations

from textual.app import App
from textual.binding import Binding

from linernotes.catalog import Catalog
from linernotes.config import Settings


class LinerNotesApp(App[None]):
    CSS_PATH = "styles/app.tcss"
    TITLE = "linernotes"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        # DECISION D3: shared state. The app holds the services (catalog, palette,
        # art cache) and MainScreen reaches them via `self.app`. The search index
        # is passed into MainScreen's constructor instead. Why might you treat
        # those two differently? (Hint: which is easier to fake in a test?)
        self.catalog: Catalog | None = None

    def on_mount(self) -> None:
        """Startup: load catalog + palette, build the artist SearchIndex, push MainScreen.

        Startup failures (missing catalog, bad palette TOML) should produce a
        readable message, not a traceback. How would you show one in Textual?
        (Look at `self.exit(message=...)` and `self.notify(...)`.)
        """
        raise NotImplementedError
