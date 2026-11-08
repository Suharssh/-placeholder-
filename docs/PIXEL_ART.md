# Black-and-white pixel art in a terminal

The palette is two colours: black and white. That one choice changes how the
portrait pipeline works:

1. **Shading comes only from dithering.** There's no grey, so mid-tones are
   patterns: more white dots = lighter. Your choice of dither algorithm *is*
   the look of every portrait.
2. **Tone control matters more than colour matching.** "Which colour is nearest"
   becomes "is this brighter than a threshold". What matters is how you measure
   brightness (`luminance`) and how you shape tones before thresholding (`preprocess`).
3. **Finer glyph encodings become free.** With colour, half blocks were the only
   way to keep exact colours per pixel. With two colours, quadrant (2×) and
   braille (4× the pixels) cost nothing in colour, so resolution is up for grabs.

## The pipeline (art/)

```
photo ─► crop ─► to_grayscale ─► preprocess ─► downscale ─► quantize ─► to_cells ─► PixelArt
                 (your           (contrast,    (to the box's  (1-bit     (half / quadrant
                  luminance)      gamma)        pixel grid)    dither)     / braille)
```

### Brightness: `luminance`
`(R+G+B)/3` treats pure blue as bright as pure green, but it looks far darker.
A saturated red shirt and a blue wall can come out the same grey and dither into
one blob. Use Rec. 709 relative luminance (on linear values) or OKLab L. Compare
with Pillow's `convert("L")` (`preview_art.py --compare-luma`).

### Tone shaping: `preprocess`
A 1-bit face reads when it has a few clear zones (shadow / mid / highlight).
Before dithering:
* **contrast** up (1.2-1.6) so shadows go solid black and highlights solid white
  (clean areas make the dithered mid-tones read as form, not noise);
* **gamma** to pull detail out of dark regions, which matters for darker skin
  tones and dark backgrounds: without it, faces collapse into a black silhouette;
* stretch: per-region autocontrast (CLAHE).
Test on several different portraits. One setting rarely fits all; per-artist
overrides in the catalog are a reasonable outcome.

### Dithering: `quantize`

| Mode | Look | Stable if animated |
|---|---|---|
| `none` (threshold) | bold poster silhouette, loses facial detail | yes |
| `ordered` (Bayer) | regular cross-hatch texture, very "computer" | yes |
| `atkinson` | classic 1-bit Macintosh look: crisp, contrasty, clean highlights | no (flickers) |
| `floyd-steinberg` | smoothest greys, but grainier/muddier in 1-bit | no (flickers) |

Why Atkinson tends to win for portraits: it only spreads 6/8 of the
quantization error, so near-white and near-black areas stay *clean* instead of
speckled. The price is some lost detail in extreme tones. The scaffold defaults to
Atkinson (`Settings.dither`).

### Glyph encoding: `render.py` (decision D2)

| Encoding | Pixels per cell | Pixel shape | Character |
|---|---|---|---|
| `half` `▀` | 1×2 | square | chunky, true "pixel art" |
| `quadrant` `▚` | 2×2 | 1:2 tall | double resolution, slightly odd diagonals |
| `braille` `⣿` | 2×4 | square dots with gaps | 4× resolution, fine dot-matrix feel |

Resolution example: a 45×45-cell box is 45×90 px in half blocks but 90×180
dots in braille. Braille portraits show far more facial detail. The gaps between
dots make them look lighter and more delicate. Half blocks look bolder and more
"pixel art". **Try both on your actual images before deciding.**

Font check (Windows Terminal): braille and quadrant glyphs must line up without
gaps or misalignment. Cascadia Mono / Cascadia Code are a good starting point;
check any font you switch to.

### Box vs pixels
`ui/layout.compute_art_box` sizes the box in *physical* screen space (cells are
~1:2), identically for every encoding. `art/pipeline.pixel_size_for_box` then
says how many pixels fit inside for the chosen encoding. Keep those two apart:
it's why switching encodings never changes the layout code.

## Choosing artist images (you pick them)

In 1-bit, image choice matters even more:
* **Tight crop** on head and shoulders. The face should fill most of the frame.
* **Strong, directional light** (one side lit, one in shadow). Flat, even lighting
  dithers into uniform grey mush.
* **Plain background**, ideally much darker or much lighter than the face.
  A busy background becomes noise competing with the face.
* Black-and-white source photos with deep contrast work beautifully.
* Artist photos are almost always someone else's copyright. Keep them local
  (`assets/artists/` is git-ignored) and don't redistribute them.

## Honest limits

Automatic photo → 1-bit gives you a striking, recognisable portrait if the
source image cooperates. It won't add what a pixel artist would: clean outlines,
selective detail, hand-placed highlights. If a portrait matters to you, run the
pipeline, then hand-clean the PNG in a pixel editor (Aseprite, or the free
Pixelorama), and have the app prefer `assets/artists/<id>.pixel.png` when it exists.
That's a reasonable hybrid; record it as an ADR if you go that way.

## Stretch ideas

* Edge pass: before dithering, darken strong luminance edges by a notch. Fake outlines
  help faces read at small sizes.
