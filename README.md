# claude-skills-hub

100 focused skills for coding agents.

This repository now ships a lean default set for code review, debugging, testing,
frontend, backend, DevOps, security, documentation, Git/GitHub, MCP, and agent
workflow tasks.

The previous full corpus is preserved at:

- Branch: `archive/full-corpus-fa85915`
- Tag: `full-corpus-fa85915`

The default branch is intentionally small. Normal installs should receive exactly
100 skills.

## Install

### Claude Code

```bash
# 🏗️ engineering
npx skills add KunanonJ/claude-skills-hub/karpathy-guidelines -g -y
npx skills add KunanonJ/claude-skills-hub/spec-driven-development -g -y
npx skills add KunanonJ/claude-skills-hub/lighthouse-agentic-browsing -g -y
npx skills add KunanonJ/claude-skills-hub/startup-cto -g -y
npx skills add KunanonJ/claude-skills-hub/expo-observe -g -y
```
npx skills add KunanonJ/claude-skills-hub -g -a claude-code -s '*' --copy -y
```

### Codex

```bash
npx skills add KunanonJ/claude-skills-hub -g -a codex -s '*' --copy -y
```

### Manual Copy

```bash
git clone --depth 1 https://github.com/KunanonJ/claude-skills-hub.git /tmp/claude-skills-hub
rsync -a /tmp/claude-skills-hub/skills/ ~/.codex/skills/
```

Use the target skill directory for your agent, such as `~/.claude/skills/` or
`~/.codex/skills/`.

## What Is Included

The retained skills are selected for coding-agent usefulness:

| Area | Examples |
| --- | --- |
| Review and debugging | `code-review`, `bug-hunter`, `systematic-debugging` |
| Testing | `test-driven-development`, `playwright`, `property-based-testing` |
| Code quality | `clean-code`, `refactoring-patterns`, `codebase-cleanup-tech-debt` |
| Documentation and architecture | `documentation`, `architecture-patterns`, `api-design-principles` |
| Frontend | `typescript-expert`, `react-patterns`, `nextjs-best-practices`, `frontend-a11y` |
| Backend | `backend-api-design`, `python-best-practices`, `fastapi-pro`, `golang-patterns` |
| Data and infrastructure | `postgresql`, `docker-patterns`, `kubernetes-patterns`, `terraform-specialist` |
| Delivery | `github-actions-advanced`, `ci-cd-patterns`, `deployment-patterns` |
| Security | `security-review`, `secrets-management`, `dependency-check`, `codeql` |
| Git, MCP, and agent workflow | `git-pr-review`, `git-worktree`, `mcp-server-patterns`, `openai-docs` |

Browse the complete set in [`skills/`](./skills/) or
[`skills-manifest.txt`](./skills-manifest.txt).

## Validation

Run the lean-corpus contract check before merging:

```bash
python -m app.skill_quality validate-lean
```

It verifies:

- `skills-manifest.txt` contains exactly 100 sorted entries.
- Every manifest entry resolves to `skills/<name>/SKILL.md`.
- No extra top-level directories exist under `skills/`.
- `skills-source-map.tsv` contains exactly 100 data rows matching the manifest.
- No broken symlinks remain under `skills/`.

Metadata can be checked separately:

```bash
python -m app.skill_quality normalize-metadata --check
```

Missing `name` or `description` frontmatter fails the check. Weak descriptions
are reported as warnings so the first prune can remain focused.

Full test commands:

```bash
uv run --with pytest --with packaging pytest -q
uv run --with ruff ruff check .
python -m app.skill_quality validate-lean
python -m app.skill_quality normalize-metadata --check
```

## Source Map

[`skills-source-map.tsv`](./skills-source-map.tsv) keeps each retained skill
traceable to the upstream source and relative path it came from. The source map is
part of the 100-skill contract and must be regenerated or edited whenever the
manifest changes.

## Full Corpus Archive

The old multi-thousand-skill corpus is not part of the default install path.
Recover it only through the archive branch or tag:

```bash
git fetch origin archive/full-corpus-fa85915 full-corpus-fa85915
git checkout archive/full-corpus-fa85915
```

Do not add full-corpus bootstrap commands or one-line shell setup scripts back to
the default README path. They belong in archive-specific documentation only.

## Contributing

The main branch is capped at exactly 100 skills. Add or replace a skill only when
it improves the coding-agent set enough to remove another skill.

Before opening a PR:

- Keep `skills-manifest.txt` sorted and exactly 100 lines.
- Keep `skills-source-map.tsv` aligned with the manifest.
- Ensure each retained skill has `SKILL.md` with `name` and `description`.
- Run the validation and test commands above.
