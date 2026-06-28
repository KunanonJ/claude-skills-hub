## Learned User Preferences

- Only create git commits when explicitly requested.
- Uses Söhne font in Cursor (editor, integrated terminal, debug console), not Test Söhne.
- Prefix shell commands with `rtk` for Headroom token savings when safe; use raw commands only for debugging.
- Configure MCP servers globally in `~/.cursor/mcp.json`; disable broken `plugin-*` duplicates in Settings → Tools & MCP and keep working user-defined entries.
- Reload Cursor (Developer: Reload Window) to pick up MCP and skills changes; full quit is rarely needed.

## Learned Workspace Facts

- Canonical GitHub repo is `https://github.com/KunanonJ/ai-skills-hub`; local workspace folder is `claude-skills-hub-lean`.
- Lean corpus ships exactly 100 skills; validate with `python -m app.skill_quality validate-lean`.
- Run tests from `.venv` with `python -m pytest`.
- Cursor global skills install: `npx skills add KunanonJ/ai-skills-hub -g -a cursor -s '*' --copy -y`.
- Full historical corpus is preserved on branch/tag `archive/full-corpus-fa85915`.
- Project-level skill mirror lives at `.agents/skills/`.
