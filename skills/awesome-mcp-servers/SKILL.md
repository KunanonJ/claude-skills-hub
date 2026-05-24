---
name: awesome-mcp-servers
description: Search, compare, and safely evaluate MCP server candidates from punkpeye/awesome-mcp-servers. Use when a task asks to find MCP servers, install an MCP from a broad catalog, compare MCP options by category, discover official/community MCP implementations, or select local/cloud MCP tooling for Codex without immediately changing config.
---

# Awesome MCP Servers

## Core Rule

Treat `punkpeye/awesome-mcp-servers` as a discovery catalog, not an installable MCP server. Do not add this repository itself to Codex MCP config. Use it to shortlist candidates, then inspect the selected server's official repo before installing anything.

The local catalog clone is installed at:

```text
/Users/kunanonjarat/.codex/sources/awesome-mcp-servers
```

## Search Workflow

1. Search the local catalog first with `scripts/search_catalog.py`.
2. Shortlist 2-5 candidates that match the user's use case, platform, and security constraints.
3. Prefer official implementations when quality and scope are otherwise comparable.
4. Prefer local servers for local files, browsers, IDEs, databases, or desktop apps; prefer cloud servers for remote SaaS APIs.
5. Before installation, open the selected server repo and verify its README, package name, config format, required secrets, transport, license, and maintenance status.
6. Never hardcode tokens in Codex config. Use wrapper scripts, existing CLIs/keychains, `.env.example`, or secret managers.
7. For destructive-capable servers such as cloud, database, browser, finance, auth, or deployment tools, classify risk and ask before enabling broad write access.
8. Verify startup or command surface before claiming an MCP server works.

## Useful Commands

Search by keyword:

```bash
python3 /Users/kunanonjarat/.codex/skills/awesome-mcp-servers/scripts/search_catalog.py database postgres
```

Filter by category and local/cloud scope:

```bash
python3 /Users/kunanonjarat/.codex/skills/awesome-mcp-servers/scripts/search_catalog.py browser --category "Browser Automation" --local
```

Find official TypeScript servers:

```bash
python3 /Users/kunanonjarat/.codex/skills/awesome-mcp-servers/scripts/search_catalog.py github --official --language typescript
```

Return JSON for downstream processing:

```bash
python3 /Users/kunanonjarat/.codex/skills/awesome-mcp-servers/scripts/search_catalog.py vector database --json --limit 20
```

## References

- Read `references/selection-policy.md` before recommending or installing candidates.
- Read `references/catalog-snapshot.md` for the installed snapshot, legend, categories, and update command.
