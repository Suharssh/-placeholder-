"""Cache rendered pixel grids so a resize or revisit doesn't redo the whole pipeline.

DECISION D4: in-memory only (functools.lru_cache / dict) vs on-disk (.art-cache/)?
Start in memory. Go to disk only if you can MEASURE a slow startup.
The hard part of caching is the key: anything that changes the output must be
in it, or you will show stale art.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from linernotes.art.palette import Palette


def cache_key(image_path: Path, palette: Palette, size: tuple[int, int], dither: str, encoding: str) -> str:
    """Stable string identifying one render.

    Must change when: the image file changes (mtime or content hash?), the
    palette's colours change (not just its name!), the size, dither mode or
    encoding changes, or your pipeline code changes (add a PIPELINE_VERSION constant).
    hashlib.sha256 over a joined string is fine.
    """
    raise NotImplementedError


class ArtCache:
    def __init__(self, directory: Path | None = None, *, max_items: int = 64) -> None:
        """directory=None means memory-only."""
        raise NotImplementedError

    def get(self, key: str) -> Image.Image | None:
        raise NotImplementedError

    def put(self, key: str, img: Image.Image) -> None:
        """Evict the least-recently-used entry past max_items (collections.OrderedDict)."""
        raise NotImplementedError
