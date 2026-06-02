---
name: transform-upscale-image-with-transloadit
description: One-off AI image upscaling (local image -> upscaled image) using Transloadit via the `transloadit` CLI. Prefer the `image upscale` intent and use `--output` for a deterministic path.
when_to_use: |
  Triggers when the user asks to upscale an image, increase image resolution, enlarge a photo without quality loss, super-resolve a picture, or enhance faces in an upscaled image. Choose this over `transform-generate-image-with-transloadit` when the input is an existing image that should be scaled up, not a prompt-driven new image. Choose this over resize when the user wants AI-based quality-preserving enlargement, not simple pixel resizing.
---

# Run

Use the `image upscale` intent for quick AI upscaling of a local image.

```bash
npx -y @transloadit/node image upscale \
  --input ./photo.jpg \
  --output ./photo-upscaled.png
```

Defaults: `--model nightmareai/real-esrgan`, `--scale 2`, `--face-enhance false`.

# Run With 4x Upscale

```bash
npx -y @transloadit/node image upscale \
  --input ./photo.jpg \
  --scale 4 \
  --output ./photo-upscaled.png
```

# Run With Face Enhancement

Use when the input contains human faces that should be sharpened. Pair with `gfpgan` or `codeformer`
for dedicated face restoration, or keep `real-esrgan` + `--face-enhance` for a general upscale that
also improves faces.

`--face-enhance` is a boolean flag — pass it bare, not with `true`.

```bash
npx -y @transloadit/node image upscale \
  --input ./portrait.jpg \
  --face-enhance \
  --output ./portrait-upscaled.png
```

# Pick A Model

- `nightmareai/real-esrgan` (default): general-purpose SOTA upscaler for photos and illustrations.
- `tencentarc/gfpgan`: specialized face restoration; best for portraits with damaged or low-quality faces.
- `sczhou/codeformer`: alternative face restoration with more control over fidelity vs. quality.

```bash
npx -y @transloadit/node image upscale \
  --input ./portrait.jpg \
  --model tencentarc/gfpgan \
  --output ./portrait-restored.png
```

Notes:
- Upscaling is an AI operation; processing time and cost scale with image size and `--scale`.
- Without `--output`, the CLI writes next to the input file using the intent's default extension.
- `--scale` only accepts `2` or `4`.

# Debug If It Fails

```bash
npx -y @transloadit/node assemblies get <assemblyIdOrUrl> -j
```

Notes:
- Upscaling robots can be account-gated; if the assembly fails with capability or availability errors, confirm `/image/upscale` is enabled for your account or switch `--model`.
- Very large inputs combined with `--scale 4` can exceed per-account limits; try `--scale 2` first.
