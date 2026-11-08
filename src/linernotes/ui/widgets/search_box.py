"""Reusable "type to search, arrow to pick, Enter to choose" widget.

It knows nothing about artists. It gets a `search` function and emits a Selected
message carrying whatever item was chosen. That keeps it reusable and easy to test.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Input

from linernotes.search import Match

SearchFn = Callable[[str], Sequence[Match[Any]]]


class SearchBox(Widget):
    class Selected(Message):
        """Posted when the user chooses a result. `item` is whatever the index holds (an Artist)."""

        def __init__(self, item: Any) -> None:
            super().__init__()
            self.item = item

    def __init__(self, search: SearchFn, *, placeholder: str = "search", id: str | None = None) -> None:
        super().__init__(id=id)
        self._search = search
        self._placeholder = placeholder

    def compose(self) -> ComposeResult:
        """An Input on top, a results list below.

        Results widget: OptionList is the natural fit (keyboard navigation for free).
        Read its docs. You'll need to map an option back to its Match.item.
        """
        raise NotImplementedError

    def on_input_changed(self, event: Input.Changed) -> None:
        """Every keystroke: run self._search(event.value), refresh the results list.

        Your search is synchronous and fast (measure it), so calling it here is fine.
        If it ever isn't, this is where a worker or a debounce goes.
        """
        raise NotImplementedError

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter in the input: choose the highlighted (or top) result, post Selected."""
        raise NotImplementedError

    def render_match_label(self, match: Match[Any]) -> str:
        """How one result row looks, in black and white: no colour to lean on.

        Use match.spans to emphasise the matched characters with bold or underline.
        CLI touch: prefix rows with "  " and the highlighted one with "> ".
        Rich markup ("[b]Kend[/b]rick") or rich.text.Text with stylize(): pick one.
        Escape user-controlled text if you use markup (rich.markup.escape).
        """
        raise NotImplementedError
