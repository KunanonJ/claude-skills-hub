---
name: transform-convert-markdown-to-pdf-with-transloadit
description: Convert a local Markdown file to a sibling PDF via the official `@transloadit/node` CLI. Use when the user wants a `.md` file rendered as a `.pdf`, especially from an agent session or local repo. The CLI resolves auth from the shell environment, the current working directory `.env`, then `~/.transloadit/credentials`.
---

# Markdown to PDF with Transloadit

## Use this for

- One local Markdown file to one local PDF file
- Keeping the PDF next to the source Markdown file
- Agent workflows where credentials may already be in the shell, a local `.env`, or
  `~/.transloadit/credentials`

## Inputs

- Absolute path to a local `.md` file
- Optional output path; default is the same path with `.pdf`

## Workflow

1. Confirm the Markdown input file exists and resolve it to an absolute path.
2. Derive the output path beside it unless the user gave a different `.pdf` target.
3. Let the CLI resolve auth automatically in this order:
   - Shell environment variables
   - The current working directory `.env` only
   - `~/.transloadit/credentials`
   If your `.env` lives in a parent directory, export the variables into the shell first.
4. Run the conversion with the official CLI:

```bash
npx -y @transloadit/node markdown pdf --input /ABS/PATH/file.md --output /ABS/PATH/file.pdf
```

## Notes

- Prefer `@transloadit/node`; it is the official CLI route and exposes `markdown pdf`.
- When no `--output` is provided, the CLI writes the PDF next to the Markdown file by default.
- Prefer `~/.transloadit/credentials` as the default fallback when you want a reusable user-level setup.
- A current-directory `.env` still takes precedence, so avoid it when deterministic account selection matters.
- If credentials only exist in a repo-root `.env`, run the command from that directory or export the variables first.
- Keep the secret server-side or local-only; never move `TRANSLOADIT_SECRET` into browser code.
- After conversion, confirm the PDF exists at the expected output path.
