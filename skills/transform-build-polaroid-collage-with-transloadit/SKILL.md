---
name: transform-build-polaroid-collage-with-transloadit
description: One-off polaroid-stack photo collage (N local images -> single image) using the official `@transloadit/node` CLI. Uses the `/image/merge` Robot's `polaroid-stack` effect and downloads the result to an explicit output path via `--output`.
when_to_use: |
  Triggers when the user asks to create a polaroid collage, build a polaroid stack, arrange photos as polaroids, make a scrapbook-style photo collage, or lay out tilted overlapping instant photos on a canvas. Choose this over the mosaic skill when the vibe is personal or scrapbook-ish (event recaps, "year in photos"), and over `transform-generate-image-with-transloadit` when the input is N existing photos rather than a text prompt.
---

# Inputs

- Two or more absolute paths to local input images
- Optional output path; default to an explicit `collage.png` in the current working directory
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
  --effect polaroid-stack \
  --width 1920 \
  --height 1200 \
  --format png \
  --output ./collage.png
```

After the command finishes, confirm the image exists at the expected output path.

# Tuning

- `--background '#eee5d3'` picks a warm beige canvas (default). Hex codes or named colors both work.
- `--background none` (with `--format png` or `--format webp`) produces a transparent canvas.
- `--coverage 1.5` is the default. Use `2.0`–`2.5` for bigger, more overlapping photos; `1.0` or below for smaller, more widely spaced polaroids.
- `--seed 42` makes the layout deterministic — rerun with the same inputs to reproduce the same output.
- `--shuffle` lets the Robot reorder inputs before laying them out.

# Debug If It Fails

```bash
npx -y @transloadit/node assemblies get <assemblyIdOrUrl> -j
```

Notes:
- Repeated `--input` values are bundled into a single `/image/merge` assembly.
- The polaroid-stack effect works best with 4–12 inputs. Fewer than four tends to look sparse; more than a dozen starts to occlude heavily.
- Each input is cropped to a square inside its polaroid frame — portrait or landscape originals both work.
- Prefer an explicit output filename (e.g. `./collage.png` or `./collage.jpg`) over a directory output so the extension is deterministic.
