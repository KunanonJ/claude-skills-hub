# Legacy Issue Guidance

Several GitHub issues were opened before the main branch became a lean
100-skill coding-agent corpus. Use this guide when triaging or reopening them.

## Current main branch policy

- Exactly **100** skills under `skills/`, focused on AI **coding-agent** workflows.
- Do **not** run `sync-listed-sources.sh` on main; it targets the archived full
  corpus workflow.
- Full corpus recovery: branch/tag `archive/full-corpus-fa85915`.

## Issue-specific notes

| Issue | Status | Resolution |
| --- | --- | --- |
| #10 Verify `skills/a*/` frontmatter | Closed | Verified 2026-06-28; all seven `a*` skills have valid frontmatter; `normalize-metadata --check` passes. |
| #11 expo-observe README examples | Closed | Lean README no longer documents per-skill cherry-pick installs; use full install commands instead. |
| #12 saas-gtm skill | Closed | Out of scope for the lean coding corpus unless an existing skill is displaced via manifest review. |
| #13 awesome-claude-code listing | Action needed | Submit via [recommend-resource issue form](https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml) (web UI only — not `gh` CLI). |
| #14 Apify marketing blog skills | Archive only | Blog templates are marketing/prospecting skills; add to `sync-listed-sources.sh` only on `archive/full-corpus-fa85915`, not on main. Source: https://use-apify.com/blog/claude-code-skills-marketing-business |

## awesome-claude-code submission text (issue #13)

Use this in the web form (update counts if the corpus changes):

- **Display name:** ai-skills-hub
- **Category:** Agent Skills
- **URL:** https://github.com/KunanonJ/ai-skills-hub
- **Description:** 100 curated SKILL.md workflows for Claude Code, Codex, Cursor, Gemini CLI, and Windsurf — focused on review, debugging, testing, backend, frontend, DevOps, security, and agent workflow tasks. Full historical corpus archived on `archive/full-corpus-fa85915`.

Install:

```bash
npx skills add KunanonJ/ai-skills-hub -g -a claude-code -s '*' --copy -y
```

## Apify blog skills (issue #14)

The blog post embeds ten marketing/business skill templates (SEO audit, lead
research, content pipeline, etc.). They are not part of the lean main branch.
To ingest them into the archived corpus:

1. Check out `archive/full-corpus-fa85915`.
2. Add the blog URL to `SOURCE_INPUTS` in `sync-listed-sources.sh`:

```python
{"kind": "page", "url": "https://use-apify.com/blog/claude-code-skills-marketing-business"},
```

3. Run `bash sync-listed-sources.sh`, reconcile manifest/source map, and open a
   PR against the archive branch — not `main`.
