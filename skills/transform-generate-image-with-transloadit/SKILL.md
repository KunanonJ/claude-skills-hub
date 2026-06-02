---
name: transform-generate-image-with-transloadit
description: One-off image generation (prompt -> image file) using Transloadit via the `transloadit` CLI. Prefer `image generate` for text-only and input-guided generation, and use `--output` when you need a deterministic path.
when_to_use: |
  Triggers when the user asks to generate an image, create an image from a prompt, make an AI image, render a picture from text, or guide image generation with reference photos. Choose this for prompt-driven or prompt+input-guided generation of a local image file. Prefer this over the collage skills when the input is a text prompt rather than N existing photos to composite.
---

# Run

Use the `image generate` intent for quick image generation from a prompt.

```bash
npx -y @transloadit/node image generate \
  --prompt 'A minimal product photo of a chameleon on white background' \
  --output ./out.png
```

# Run With OpenAI gpt-image-2

Use this when the user explicitly asks for `openai/gpt-image-2`, `gpt-image-2`, or OpenAI image
generation. Keep it opt-in for now; the CLI default remains `google/nano-banana-2`.

```bash
npx -y @transloadit/node image generate \
  --model openai/gpt-image-2 \
  --width 1024 \
  --height 1024 \
  --prompt 'A ceramic coffee mug on a white seamless studio background' \
  --output ./out.png
```

# Run With Input Images

You can also guide generation with one or more input images. Prefer meaningful filenames and refer
to them in the prompt.

```bash
npx -y @transloadit/node image generate \
  --input ./person1.jpg \
  --input ./person2.jpg \
  --input ./background.jpg \
  --prompt 'Place person1.jpg feeding person2.jpg in front of background.jpg' \
  --output ./out.png
```

Notes:
- The CLI defaults to `google/nano-banana-2`.
- Use `--model openai/gpt-image-2` for OpenAI image generation. The older `gpt-image-2` spelling is
  still accepted by API2 for backwards compatibility.
- Repeated `--input` values are bundled into a single `/image/generate` assembly.
- Prompt-only generation still works without any `--input`.
- Without `--output`, prompt-only and multi-input runs default to the current working directory.

# Debug If It Fails

```bash
npx -y @transloadit/node assemblies get <assemblyIdOrUrl> -j
```

Notes:
- Some generator/AI robots can be account-gated; if the assembly fails with capability or
  availability errors, switch models or confirm the feature is enabled for your account.
