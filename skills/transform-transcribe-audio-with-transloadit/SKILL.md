---
name: transform-transcribe-audio-with-transloadit
description: One-off transcription of local audio or video files to text or subtitle files using Transloadit via the official `@transloadit/node` CLI. Use when the user wants speech in local media converted to `.txt`, `.json`, `.srt`, or `.webvtt`; prefer the `speech transcribe` intent with Replicate while ElevenLabs Scribe is not ready.
---

# Transcribe Audio or Video with Transloadit

## Use this for

- Local audio or video files that should become text transcripts or subtitle files
- One or many files, with outputs downloaded locally
- Agent workflows where credentials may already be in the shell, a local `.env`, or
  `~/.transloadit/credentials`

## Inputs

- Absolute path to one or more local audio or video files
- Optional output path; default is the same basename with `.txt`
- Optional format: `text`, `json`, `srt`, or `webvtt`

## Workflow

1. Confirm each input file exists and resolve it to an absolute path.
2. Derive the output path:
   - Single input and no requested output: same directory and basename with `.txt`
   - Multiple inputs and no requested output: a `transcripts/` directory next to the inputs
   - Use `.json`, `.srt`, or `.webvtt` when the user asks for that format
3. Let the CLI resolve auth automatically in this order:
   - Shell environment variables
   - The current working directory `.env` only
   - `~/.transloadit/credentials`
   If your `.env` lives in a parent directory, export the variables into the shell first.
4. Run the transcription with the official CLI intent:

```bash
npx -y @transloadit/node speech transcribe --input /ABS/PATH/input.opus --output /ABS/PATH/input.txt
```

For multiple files, repeat `--input` and write to an output directory:

```bash
npx -y @transloadit/node speech transcribe \
  --input /ABS/PATH/a.opus \
  --input /ABS/PATH/b.opus \
  --output /ABS/PATH/transcripts/
```

## Options

- Default format: `text`
- Other formats: `--format json`, `--format srt`, `--format webvtt`
- Default provider: `replicate` until ElevenLabs Scribe is ready
- Supported explicit providers: `--provider aws`, `--provider gcp`, `--provider replicate`
- Do not use `--provider transloadit`; that internal Whisper route is work in progress
- Use `--source-language <code>` when the input language is known
- Use `--target-language <code>` when translation is requested

## Notes

- Prefer `@transloadit/node`; it is the official CLI route and exposes `speech transcribe`.
- If the command errors with a missing subcommand, update to a newer `@transloadit/node` release
  that includes the speech transcription intent.
- Keep secrets local-only; never print `TRANSLOADIT_SECRET` or copy it into browser code.
- After transcription, confirm each expected output file exists and is non-empty.
