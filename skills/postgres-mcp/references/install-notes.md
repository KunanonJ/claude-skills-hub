# Postgres MCP Install Notes

## Source

- Repository: https://github.com/crystaldba/postgres-mcp
- Installed package entry point: `uvx postgres-mcp`
- Verified source revision during install: `07eb329c8c48e49640e0d1b5b35465d4d024c3ee`

## Local Codex Integration

Codex uses `/Users/kunanonjarat/.codex/bin/postgres-mcp-safe.sh` instead of putting secrets directly in `/Users/kunanonjarat/.codex/config.toml`.

The wrapper:

- passes through `--help` without requiring credentials,
- optionally loads `$HOME/.codex/secrets/postgres-mcp.env`,
- requires `POSTGRES_MCP_DATABASE_URI`,
- defaults to `POSTGRES_MCP_ACCESS_MODE=restricted`,
- rejects any access mode other than `restricted` or `unrestricted`,
- launches `uvx postgres-mcp --access-mode "$POSTGRES_MCP_ACCESS_MODE" "$POSTGRES_MCP_DATABASE_URI"`.

## Database Credential Setup

Create the env file manually if persistent local credentials are needed:

```bash
mkdir -p "$HOME/.codex/secrets"
chmod 700 "$HOME/.codex/secrets"
$EDITOR "$HOME/.codex/secrets/postgres-mcp.env"
```

Expected content:

```bash
POSTGRES_MCP_DATABASE_URI='postgresql://readonly_user:password@host:5432/database'
POSTGRES_MCP_ACCESS_MODE='restricted'
```

Do not commit this file and do not paste real values into chat.

## Access Mode

- `restricted`: default. Use for production-like databases and normal Codex analysis.
- `unrestricted`: write-capable. Use only for disposable development databases or after explicit user approval.

## Optional Extensions

Some deeper analysis is more useful when the database has:

- `pg_stat_statements` for workload/top-query analysis.
- `hypopg` for hypothetical index simulation.

Do not install extensions on shared or production databases without explicit approval.
