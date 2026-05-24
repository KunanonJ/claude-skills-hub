# Installed Catalog Snapshot

## Source

- Repository: `https://github.com/punkpeye/awesome-mcp-servers`
- Local path: `/Users/kunanonjarat/.codex/sources/awesome-mcp-servers`
- Installed commit: `39b5e990fe94734de271a2b13ec1513811da9cdd`
- Snapshot date: `2026-05-24`
- README size at install: 2,628 lines
- Parsed at install: 2,237 server entries across 49 sections

## Update Command

Refresh the local catalog when the user asks for latest MCP server options:

```bash
git -C /Users/kunanonjarat/.codex/sources/awesome-mcp-servers fetch --depth 1 origin main
git -C /Users/kunanonjarat/.codex/sources/awesome-mcp-servers reset --hard origin/main
```

Only this local source clone should be reset by the update command. Do not use broad destructive git commands in user project repositories.

## Legend

The catalog uses markers for implementation type and deployment scope:

- Official implementation: trophy marker.
- Languages: Python, TypeScript/JavaScript, Go, Rust, C#, Java, C/C++, Ruby.
- Scope: cloud service, local service, embedded system.
- OS: macOS, Windows, Linux.

## Main Categories

Examples of major sections include:

- Aggregators
- Browser Automation
- Cloud Platforms
- Code Execution
- Coding Agents
- Command Line
- Communication
- Databases
- Data Platforms
- Developer Tools
- File Systems
- Finance and Fintech
- Knowledge and Memory
- Monitoring
- OS Automation
- Search and Data Extraction
- Security
- Version Control
- Workplace and Productivity

Use `scripts/search_catalog.py --list-categories` for the current full category list.
