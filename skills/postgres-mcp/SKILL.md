---
name: postgres-mcp
description: Use Crystal DBA Postgres MCP Pro for PostgreSQL schema inspection, safe read-only SQL, explain plans, health checks, and index-tuning analysis from Codex. Trigger when the user asks for postgres-mcp, Postgres MCP Pro, PostgreSQL MCP database analysis, SQL explain/index tuning via MCP, or troubleshooting the local crystaldba/postgres-mcp install.
---

# Postgres MCP

## Core Rule

Use the local `postgres-mcp` Codex MCP server for PostgreSQL analysis only when the user has provided or configured an explicit database connection string. Never ask the user to paste database credentials into chat and never hardcode connection strings in Codex config, skills, scripts, or logs.

The Codex MCP server is configured as:

```toml
[mcp_servers.postgres-mcp]
command = "/Users/kunanonjarat/.codex/bin/postgres-mcp-safe.sh"
startup_timeout_sec = 60
tool_timeout_sec = 300
```

The wrapper reads `POSTGRES_MCP_DATABASE_URI` from the parent environment or from `$HOME/.codex/secrets/postgres-mcp.env` if that file exists. The default access mode is `restricted`.

## Safety Policy

1. Prefer a read-only database user, a staging database, or a disposable snapshot.
2. Use `POSTGRES_MCP_ACCESS_MODE=restricted` by default. Restricted mode exposes read-only SQL behavior and a timeout.
3. Do not use `POSTGRES_MCP_ACCESS_MODE=unrestricted` unless the user explicitly approves write-capable database access for the specific environment.
4. Treat production database access as high risk. Confirm the database target and intended operations before running schema-changing, data-changing, expensive, or broad health/index analysis.
5. Redact passwords and tokens from all output. If a command prints a connection string, stop and replace it with a redacted form before reporting.

## Available Tool Surface

Postgres MCP Pro exposes MCP tools for:

- `list_schemas`
- `list_objects`
- `get_object_details`
- `execute_sql`
- `explain_query`
- `get_top_queries`
- `analyze_workload_indexes`
- `analyze_query_indexes`
- `analyze_db_health`

Use schema and object inspection before writing SQL. Use `explain_query` before recommending indexes for a specific query. Use workload and health tools only when the database has the required extensions and the user understands the expected load.

## Local Usage

Set credentials outside chat:

```bash
mkdir -p "$HOME/.codex/secrets"
chmod 700 "$HOME/.codex/secrets"
$EDITOR "$HOME/.codex/secrets/postgres-mcp.env"
```

Expected env file shape:

```bash
POSTGRES_MCP_DATABASE_URI='postgresql://readonly_user:password@host:5432/database'
POSTGRES_MCP_ACCESS_MODE='restricted'
```

For a one-off shell session:

```bash
export POSTGRES_MCP_DATABASE_URI='postgresql://readonly_user:password@host:5432/database'
export POSTGRES_MCP_ACCESS_MODE='restricted'
```

Then restart Codex so the MCP registry reloads the server configuration.

## Troubleshooting

1. Confirm the package entry point works with `uvx postgres-mcp --help`.
2. Confirm the wrapper refuses to start without `POSTGRES_MCP_DATABASE_URI`.
3. Confirm the configured database URI works with `psql` or another trusted client before blaming MCP.
4. If the server starts but tools fail, check database privileges, `pg_stat_statements`, `hypopg`, network access, and whether the database host is reachable from the Codex process.
5. For Docker-based databases on macOS, prefer connecting to `127.0.0.1` with the published host port from the host-side wrapper.

## References

- Read `references/install-notes.md` before changing the local config or troubleshooting startup.
