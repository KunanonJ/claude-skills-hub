# Gate Keyword Alias Contract

Wave83 establishes the minimum contract for reliable verify gates and keyword alias checks.
Every Wave83-100 gate must satisfy this checklist before it is treated as stop-ship evidence.

## Checklist

- Use `Write-VgoUtf8NoBomText` for markdown, JSON, and emitted gate reports.
- Keep YAML frontmatter at byte 0; do not prepend UTF-8 BOM before `---`.
- Treat `trigger_keywords` and alias maps as discoverability metadata, not as routing authority.
- Require execution-context lock from `vibe-governance-helpers.ps1` for governance and verify scripts.
- Register the gate in release docs and `release-cut.ps1` before calling it release-critical.
