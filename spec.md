# Install mattpocock/skills

## Requirements

- Add `mattpocock/skills` as a managed source in `sync-listed-sources.sh`.
- Regenerate `skills/`, `skills-manifest.txt`, and `skills-source-map.tsv` using the existing corpus sync flow.
- Preserve existing first-source-wins behavior for skill name collisions.
- Keep every installed skill traceable to its upstream repo and relative path.
- Do not introduce secrets or environment variables.

## Data Model

- Source input: `{"kind": "repo", "repo": "mattpocock/skills"}`.
- Skill artifact: a directory under `skills/<skill-name>/` containing `SKILL.md` and any supporting files.
- Manifest row: one skill name per line in `skills-manifest.txt`.
- Source map row: tab-separated `skill_name`, `repo_spec`, `relative_path`, and `discovered_from`.

## Edge Cases

- If a Matt Pocock skill name collides with an earlier source, the earlier source remains authoritative.
- Deprecated or in-progress upstream skills are included unless explicitly added to `SKIP_SKILLS`.
- If the upstream repo is unavailable, the existing sync script skips it with a diagnostic rather than corrupting existing source-map format.
- Supporting files inside upstream skill directories must be copied along with `SKILL.md`.

## Testing Strategy

- Add focused pytest coverage for the new managed source and generated artifacts.
- Verify that representative Matt Pocock skills are present in `skills/`, listed in `skills-manifest.txt`, and traced in `skills-source-map.tsv`.
- Run the existing required checks: `ruff check .`, `pytest -v`, and `mypy app/ --strict`.

## Task Plan

### Task 1: Register and sync `mattpocock/skills`

- Intended behavior: the corpus sync includes all non-colliding `SKILL.md` directories from `mattpocock/skills`.
- Test names:
  - `test_mattpocock_skills_source_is_registered`
  - `test_mattpocock_skills_are_installed_and_traceable`
- Affected files:
  - `sync-listed-sources.sh`
  - `skills/`
  - `skills-manifest.txt`
  - `skills-source-map.tsv`
  - `tests/test_mattpocock_skills.py`
- Risk tier: R2, because this is a reversible source-list and generated-corpus update.
- Rollback strategy: remove the source entry, rerun `bash sync-listed-sources.sh`, delete the tests/spec if no longer needed, and recommit.
