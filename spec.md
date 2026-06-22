# Lean 100-Skill Contract

## Goal

Make the main branch a focused distribution of exactly 100 AI-coding-agent
skills. The previous full corpus remains recoverable through an archive branch
and tag, but default installs, docs, manifest, and source map expose only the
lean set.

## Archive Point

- Branch: `archive/full-corpus-fa85915`
- Tag: `full-corpus-fa85915`

Both point at commit `fa85915`.

## Data Model

- Skill directory: `skills/<skill-name>/`
- Skill entrypoint: `skills/<skill-name>/SKILL.md`
- Manifest: `skills-manifest.txt`, one sorted skill name per line
- Source map: `skills-source-map.tsv`, header plus one row per retained skill

## Invariants

- `skills-manifest.txt` has exactly 100 entries.
- The manifest equals the approved lean keep list.
- Every manifest entry has `skills/<name>/SKILL.md`.
- No extra top-level directories exist under `skills/`.
- `skills-source-map.tsv` has exactly 100 data rows.
- Source-map skill names match the manifest.
- No broken symlinks exist under `skills/`.
- Each retained `SKILL.md` has `name` and `description` frontmatter.

## Validation

```bash
python -m app.skill_quality validate-lean
python -m app.skill_quality normalize-metadata --check
uv run --with pytest --with packaging pytest -q
uv run --with ruff ruff check .
```

`validate-lean` enforces the repository contract. Metadata normalization check
blocks missing required fields and warns about weak descriptions.

## Install Contract

Default installs should receive exactly 100 skills:

```bash
npx skills add KunanonJ/ai-skills-hub -g -a codex -s '*' --copy -y
```

The README must not promote full-corpus bootstrap commands or `bash <(curl ...)`
setup as the default path.

## Changing The Set

The main branch is capped at 100 skills. Adding one skill requires removing or
replacing another skill and updating both manifest files. Use the archive branch
or tag for full-corpus recovery instead of reintroducing broad sync behavior to
main.
