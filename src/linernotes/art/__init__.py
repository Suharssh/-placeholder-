"""Art pipeline: your chosen photo -> palette-limited pixel art -> terminal cells.

    source image
      -> crop to target aspect           (pixelate.crop_to_aspect)
      -> preprocess: contrast/saturation (pixelate.preprocess)
      -> downscale to the pixel grid     (pixelate.downscale)
      -> map to YOUR palette (+dither)   (pixelate.quantize)
      -> pack 2 vertical px per cell     (render.to_cells)
      -> CellGrid                        (ui/widgets/pixel_art.py draws it)

This package imports Pillow but NEVER Textual. It returns plain data (CellGrid),
so you can test it without a terminal and preview it with scripts/preview_art.py.
Read docs/PIXEL_ART.md first.
"""
