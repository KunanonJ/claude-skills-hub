---
name: transform-build-mosaic-collage-with-transloadit
description: One-off justified mosaic photo collage (N local images -> single image) using the official `@transloadit/node` CLI. Uses the `/image/merge` Robot's `mosaic` effect to build a tiled layout that keeps every photo fully visible, and downloads the result to an explicit output path via `--output`.
when_to_use: |
  Triggers when the user asks to create a mosaic collage, tile photos edge-to-edge, build a justified photo grid, make a Flickr-style photo layout, or compose N photos into a clean editorial collage that keeps every photo fully visible. Choose this over the polaroid skill when the vibe is clean and editorial (product grids, portfolio hero sections, social previews from a batch), and over `transform-generate-image-with-transloadit` when the input is N existing photos rather than a text prompt.
---

# Inputs

- Two or more absolute paths to local input images
- Optional output path; default to an explicit `collage.jpg` in the current working directory
- Optional canvas size (`--width`, `--height`), default `1920×1200`
- Optional `--seed` for deterministic layout

# Prepare Instructions

Resolve credentials in this order:
- Shell environment variables
- The current working directory `.env` only
- `~/.transloadit/credentials`

If your `.env` lives in a parent directory, export the variables into the shell first.

# Run

```bash
npx -y @transloadit/node image merge \
  --input ./photo-a.jpg \
  --input ./photo-b.jpg \
  --input ./photo-c.jpg \
  --input ./photo-d.jpg \
  --input ./photo-e.jpg \
  --input ./photo-f.jpg \
  --effect mosaic \
  --width 1920 \
  --height 1200 \
  --border 12 \
  --shuffle \
  --format jpg \
  --output ./collage.jpg
```

After the command finishes, confirm the image exists at the expected output path.

# Tuning

- `--border 12` sets both the outer canvas padding and the gutter width between tiles. Larger values give more breathing room.
- `--background '#eee5d3'` fills the gutters and canvas padding (default). Hex codes or named colors both work.
- `--background none` (with `--format png` or `--format webp`) produces a transparent canvas and transparent gutters.
- `--shuffle` lets the Robot reorder inputs before solving the layout; combine with `--seed` to pin the shuffle.
- `--seed 42` makes the mosaic solver deterministic — rerun with the same inputs to reproduce the same output.

# Debug If It Fails

```bash
npx -y @transloadit/node assemblies get <assemblyIdOrUrl> -j
```

Notes:
- Repeated `--input` values are bundled into a single `/image/merge` assembly.
- The mosaic effect reads each input's aspect ratio and solves for a justified tile layout — portrait + landscape mixes generally produce more interesting layouts than uniform sizes.
- Unlike the polaroid-stack effect, tiles are center-cropped to fit their allocated rectangle. Any portion of a photo can be cropped off — if every pixel matters, resize beforehand with `/image/resize` and `resize_strategy: fit`.
- Prefer an explicit output filename (e.g. `./collage.jpg` or `./collage.png`) over a directory output so the extension is deterministic.
