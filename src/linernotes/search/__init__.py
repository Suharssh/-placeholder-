"""The search engine. Pure Python, no UI imports, fully unit-testable.

Pipeline for one query:

    raw text --normalize--> tokens --candidates--> scored --rank--> top N Match

Build it in this order: normalize.py -> fuzzy.py -> index.py.
"""

from linernotes.search.index import Match, SearchIndex

__all__ = ["Match", "SearchIndex"]
