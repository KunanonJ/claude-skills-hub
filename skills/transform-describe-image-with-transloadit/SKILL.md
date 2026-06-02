---
name: transform-describe-image-with-transloadit
description: One-off image description using the official `@transloadit/node` CLI. Use `image describe --fields labels` for object-style labels, or `image describe --for wordpress` for structured alt text, title, caption, and description JSON.
---

# Inputs

- Absolute path to a local input image
- Optional `.json` output path; default is the same path with `.json`

# Prepare

Resolve credentials in this order:
- Shell environment variables
- The current working directory `.env` only
- `~/.transloadit/credentials`

If your `.env` lives in a parent directory, export the variables into the shell first.

# Run

Use the official Transloadit Node CLI directly.

Labels / object-style description:

```bash
npx -y @transloadit/node image describe \
  --input ./input.jpg \
  --fields labels \
  --output ./labels.json
```

WordPress-ready fields:

```bash
npx -y @transloadit/node image describe \
  --input ./input.jpg \
  --for wordpress \
  --output ./fields.json
```

Custom field selection:

```bash
npx -y @transloadit/node image describe \
  --input ./input.jpg \
  --fields altText,title,caption,description \
  --output ./fields.json
```

If you omit `--output`, the CLI writes the JSON file next to the input image using the same base
name. After the command finishes, confirm the JSON file exists at the expected output path.

# Output Shapes

`--fields labels` returns a JSON array of labels.

`--for wordpress` and authored `--fields ...` return a JSON object with requested string fields, for example:

```json
{
  "altText": "...",
  "title": "...",
  "caption": "...",
  "description": "..."
}
```

# Notes

- Prefer `--for wordpress` when you want publishable CMS fields.
- Prefer `--fields labels` when you want recognizer-style tags instead of authored copy.
- `--model` only matters for authored fields, not for `labels`.
- Prefer `~/.transloadit/credentials` as the default fallback when you want a reusable user-level setup.
- A current-directory `.env` still takes precedence, so avoid it when deterministic account selection matters.
- If credentials only exist in a repo-root `.env`, run the command from that directory or export the variables first.

# Debug If It Fails

```bash
npx -y @transloadit/node assemblies get <assemblyIdOrUrl> -j
```
