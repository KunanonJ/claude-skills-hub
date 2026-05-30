---
name: cloudflare-plugin
description: Official Cloudflare plugin for Claude Code — 8 auto-loading skills (Workers, Agents SDK, Durable Objects, Sandbox, Wrangler, email, web perf, best practices) + MCP servers for live API access, docs, and observability. Use when building on Cloudflare, Workers, KV, D1, R2, or deploying AI agents.
license: Apache-2.0
metadata:
  author: KunanonJ
  version: "1.0"
  source: https://github.com/cloudflare/skills
---

# cloudflare-plugin

Official Cloudflare plugin for Claude Code. Installs 8 auto-loading skills and multiple MCP servers for building on the Cloudflare Developer Platform.

## Install

```bash
# Inside Claude Code:
/plugin marketplace add cloudflare/skills
/plugin install cloudflare@cloudflare
```

Or via CLI:
```bash
claude plugin marketplace add cloudflare/skills
claude plugin install cloudflare@cloudflare
```

## What Gets Installed

### 8 Skills (auto-loaded based on context)

| Skill | Triggers when you ask about |
|-------|----------------------------|
| `cloudflare` | Workers, Pages, KV, D1, R2, Workers AI, Vectorize, WAF, Terraform |
| `agents-sdk` | Stateful AI agents, scheduling, RPC, MCP servers, email, streaming chat |
| `durable-objects` | Stateful coordination, chat rooms, games, SQLite, WebSockets, alarms |
| `sandbox-sdk` | Secure code execution, AI interpreters, CI/CD, interactive dev environments |
| `wrangler` | Wrangler CLI commands, `wrangler.toml` / `wrangler.jsonc` config |
| `cloudflare-email-service` | Transactional email via Email Workers |
| `workers-best-practices` | Code quality, patterns, common pitfalls |
| `web-perf` | Performance analysis, Core Web Vitals, edge optimization |

### 2 Slash Commands

| Command | Purpose |
|---------|---------|
| `/cloudflare:build-agent` | Scaffold a stateful AI agent on Cloudflare using the Agents SDK |
| `/cloudflare:build-mcp` | Build an MCP server deployed on Cloudflare Workers |

### MCP Servers

Provides live tool access for:
- **Cloudflare API** — manage Workers, KV, D1, R2, etc.
- **Cloudflare Docs** — search latest documentation
- **Bindings** — inspect and configure resource bindings
- **Builds** — trigger and monitor Workers builds
- **Observability** — logs, traces, and metrics

## Usage

Works best from a Workers project root (where `wrangler.jsonc` exists):

```bash
cd my-workers-project
claude
```

Skills activate automatically when you mention relevant Cloudflare topics. No manual invocation needed.

### Example Prompts

```
"Set up GitHub Actions to deploy this Worker on push to main"
"Create a D1 database with CRUD endpoints"
"Build an R2 upload service with presigned URLs"
"Configure KV namespace for session storage"
"Connect this Worker to Postgres via Hyperdrive"
"Deploy with a custom domain"
"Build a stateful AI agent using Agents SDK"
"Create an MCP server on Cloudflare Workers"
```

## Verify Installation

```bash
claude mcp list   # Should show cloudflare MCP servers
```

First tool call will trigger OAuth authorization for the Cloudflare API.

> **CI/CD note:** For automated pipelines, use Cloudflare API tokens instead of OAuth.

## References

- [cloudflare/skills repo](https://github.com/cloudflare/skills)
- [Cloudflare agent setup for Claude Code](https://developers.cloudflare.com/agent-setup/claude-code/)
- [Claude Code plugin marketplace](https://code.claude.com/docs/en/discover-plugins)
- [Cloudflare Developer Docs](https://developers.cloudflare.com/)
