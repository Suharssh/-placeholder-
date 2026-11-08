"""The only screen. Two states, one layout, toggled by a CSS class.

STATE 1: idle (no artist yet). The search bar is centred.

    ┌──────────────────────────────────────────────────────┐
    │                                                      │
    │                                                      │
    │                 > kend█                              │  <- SearchBox, centred
    │                   Kendrick Lamar                     │  <- live results
    │                                                      │
    │                                                      │
    └──────────────────────────────────────────────────────┘

STATE 2: showing an artist. The search bar moves to the top-left and the art
fills the middle with equal padding on all sides.

    ┌──────────────────────────────────────────────────────┐
    │ > search█                                            │  <- SearchBox, top-left
    │                                                      │
    │          ┌────────────────────────────────┐          │
    │          │▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│          │
    │          │▀▀▀▀▀▀▀  1-bit portrait  ▀▀▀▀▀▀▀│          │  <- PixelArt, centred
    │          │▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│          │
    │          └────────────────────────────────┘          │
    │                                                      │
    └──────────────────────────────────────────────────────┘

Typing in the top-left bar searches again. Its results drop down OVER the art.
Choosing a new artist swaps the art. Esc clears the artist and goes back to state 1.

Why one screen and not two? The search bar is the same widget in both states,
with the same focus and the same typed text. Pushing a second screen would mean
rebuilding it. One screen plus a CSS class (`-showing`) just moves it.
(DECISION D3: write down this reasoning in your own words.)

Layout decisions you'll make here:
  * Layers: put the SearchBox on a layer ABOVE the art (TCSS `layers`), so its
    dropdown can overlap the portrait without pushing anything around.
  * Equal padding vs the corner bar: the art must not sit under the search bar.
    Simplest rule that keeps padding equal on all four sides: use
    margin = max(settings.art_margin_cells, search bar height + 1) in
    layout.compute_art_box. The bar then lives inside the top margin.
  * The move itself: an instant jump (just the class toggle), or animated?
    Textual can animate styles (`widget.styles.animate("offset", ...)`). Do the
    instant version first. Animation is a stretch goal.
"""

from __future__ import annotations

from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen

from linernotes.domain import Artist
from linernotes.search import SearchIndex
from linernotes.ui.widgets.search_box import SearchBox


class MainScreen(Screen[None]):
    BINDINGS = [Binding("escape", "clear", "Clear")]

    # None = idle (state 1); an Artist = showing (state 2).
    artist: reactive[Artist | None] = reactive(None)

    def __init__(self, index: SearchIndex[Artist]) -> None:
        super().__init__()
        self._index = index

    def compose(self) -> ComposeResult:
        """Yield the SearchBox and the PixelArt widget.

        Both always exist. In state 1, PixelArt is hidden (TCSS `display: none`
        under `MainScreen:not(.-showing)`), so there's no widget creation or
        destruction when switching states: CSS does it all.
        """
        raise NotImplementedError

    def on_mount(self) -> None:
        """Focus the search input so the user can type immediately."""
        raise NotImplementedError

    def on_search_box_selected(self, message: SearchBox.Selected) -> None:
        """An artist was picked: self.artist = message.item.

        Should the input text clear after choosing, or keep the artist's name?
        Try both and see which feels better for searching again.
        """
        raise NotImplementedError

    def watch_artist(self, old: Artist | None, new: Artist | None) -> None:
        """React to the state change. This is the heart of the screen.

          None -> Artist:   add the "-showing" class (moves the bar via CSS), render art
          Artist -> Artist: keep the class, render the new art
          Artist -> None:   remove the class (bar returns to centre), clear the art

        Use self.set_class(new is not None, "-showing").
        Artist with no image / missing file: decide what to show (placeholder? notify?).
        """
        raise NotImplementedError

    def action_clear(self) -> None:
        """Esc: back to state 1. If already idle, maybe clear the input text instead."""
        raise NotImplementedError

    def on_resize(self, event: events.Resize) -> None:
        """Terminal resized while showing an artist -> recompute the Box -> re-render.

        Resizing by dragging fires MANY events. Rendering on each one wastes work.
        Look up "debounce", then see how Textual's set_timer can implement it.
        """
        raise NotImplementedError

    def request_render(self) -> None:
        """Compute the Box (layout.compute_art_box, margin rule above), then start a
        worker that calls art.pipeline.render_art(...) and hands the CellGrid to PixelArt.

        Use @work(thread=True, exclusive=True) so a newer request (new artist,
        new size) cancels an older one still running.
        Thread workers cannot touch widgets directly. Find out how Textual lets a
        thread hand results back (call_from_thread, or post a message).
        """
        raise NotImplementedError
