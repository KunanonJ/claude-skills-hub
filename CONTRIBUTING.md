# Contributing to claude-skills-hub

The default branch is a lean 100-skill product for coding agents. Contributions
should improve that focused set, not expand the repository back into a broad
corpus.

## Contribution Rules

- Keep exactly 100 top-level directories under `skills/`.
- Keep `skills-manifest.txt` sorted and exactly 100 lines.
- Keep `skills-source-map.tsv` aligned with the manifest.
- Every retained skill must have `skills/<name>/SKILL.md`.
- Every `SKILL.md` must have frontmatter with `name` and `description`.
- Do not add secrets, credentials, or prompt-control instructions.
- Do not restore full-corpus install instructions to the default README.

## Adding Or Replacing A Skill

Because the main branch is capped at 100 skills, adding a skill means replacing
an existing one.

1. Add or update `skills/<skill-name>/SKILL.md`.
2. Remove the displaced skill directory.
3. Update `skills-manifest.txt`.
4. Update `skills-source-map.tsv`.
5. Run the lean validation commands.

Prefer skills that directly help coding agents with review, debugging, testing,
frontend, backend, DevOps, security, documentation, Git/GitHub, MCP, or agent
workflow.

## Quality Bar

A good skill has:

- One clear trigger for when the agent should use it.
- Concrete workflow instructions.
- Bounded references, scripts, or templates only when they help.
- No broad persona text, vague encouragement, or stale external assumptions.
- A description that starts with a clear activation phrase, ideally
  `This skill should be used when ...`.

## Validation

Run:

```bash
python -m app.skill_quality validate-lean
python -m app.skill_quality normalize-metadata --check
uv run --with pytest --with packaging pytest -q
uv run --with ruff ruff check .
```

`validate-lean` is blocking. `normalize-metadata --check` blocks missing
frontmatter fields and reports weak descriptions as warnings.

## Full Corpus

The old full corpus is recoverable from:

- Branch: `archive/full-corpus-fa85915`
- Tag: `full-corpus-fa85915`

Do not use `sync-listed-sources.sh` or one-line shell bootstrap flows for normal
main-branch contributions. Those workflows are archival and can reintroduce the
large corpus.
