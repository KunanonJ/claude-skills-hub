# Codex Skill Updater

A community-curated collection of **3,000+ AI coding skills** for Claude Code, Codex, Cursor, Gemini CLI, and other coding agents — plus the automation that keeps it fresh.

## What's inside

| Resource | Count |
|---|---|
| Skills (browsable in [`skills/`](./skills/)) | 3,000+ |
| Source repos tracked | 24+ |
| Discovery pages crawled | 6 |
| Plugins (Claude Code marketplace) | 8 |
| MCP servers | 9 |

Skills are synced from the source repos listed below. Browse [`skills/`](./skills/) to see everything, or use [`skills-source-map.tsv`](./skills-source-map.tsv) to trace any skill back to its origin repo.

---

## Quick install

### Install all skills at once

```bash
npx skills add KunanonJ/codex-skill-updater -g -y
```

> This installs every skill in the `skills/` directory globally into your agent's skills folder (`~/.agents/skills/` for Claude Code).

### Install a specific skill

Browse [`skills/`](./skills/), pick what you want, then:

```bash
npx skills add KunanonJ/codex-skill-updater/<skill-name> -g -y
# example:
npx skills add KunanonJ/codex-skill-updater/karpathy-guidelines -g -y
```

### Full environment setup (skills + plugins + MCPs)

To replicate the complete environment — all 24 skill repos, 8 plugins, and 9 MCP servers — use the companion setup script:

```bash
bash <(curl -fsSL https://gist.githubusercontent.com/KunanonJ/f7e7c9b8c45d927ae03b84b1879d384d/raw/setup-claude.sh)
```

---

## Skill sources

Skills are pulled from these repos (first-source-wins on name conflicts):

| Repo | Category |
|---|---|
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Composio ecosystem |
| [ComposioHQ org repos](https://github.com/ComposioHQ) | Composio ecosystem |
| [obra/superpowers](https://github.com/obra/superpowers) | Workflow orchestration |
| [FlorianBruniaux/claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) | General |
| [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | Community |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | Memory / context |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | General |
| [anthropics/skills](https://github.com/anthropics/skills) | Official Anthropic |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Token efficiency |
| [ericvtheg/solo-founder-toolkit](https://github.com/ericvtheg/solo-founder-toolkit) | Founder |
| [ognjengt/founder-skills](https://github.com/ognjengt/founder-skills) | Founder |
| [dazuck/operator-skills](https://github.com/dazuck/operator-skills) | Operator |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | General |
| [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) | Founder |
| [Exploration-labs/Nates-Substack-Skills](https://github.com/Exploration-labs/Nates-Substack-Skills) | Writing |
| [kubony/claude-session-wrap](https://github.com/kubony/claude-session-wrap) | Session management |
| [team-attention/plugins-for-claude-natives](https://github.com/team-attention/plugins-for-claude-natives) | Plugins |
| [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) | Automation |
| [mylukin/agent-foreman](https://github.com/mylukin/agent-foreman) | Agent orchestration |
| [muratcankoylan/ralph-wiggum-marketer](https://github.com/muratcankoylan/ralph-wiggum-marketer) | Marketing |
| [ruvnet/ruflo](https://github.com/ruvnet/ruflo) | Orchestration |
| [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | Best practices |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | Best practices |
| [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) | Token compression |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Dev lifecycle |

Plus skills discovered from curated pages: [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code), [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills), [awesomeclaude.ai](https://awesomeclaude.ai/awesome-claude-skills), and more.

---

## Claude Code plugins

Install these from the Claude Code marketplace:

```bash
claude plugin install typescript-lsp
claude plugin install security-guidance
claude plugin install code-review
claude plugin install playwright
claude plugin install context7
claude plugin install pr-review-toolkit
claude plugin install feature-dev
claude plugin install ralph-loop
```

---

## MCP servers

Add these to Claude Code (no API key required):

```bash
claude mcp add --transport stdio investor-agent -- npx -y investor-agent
claude mcp add --transport stdio exa            -- npx -y exa-mcp-server
claude mcp add --transport stdio context7       -- npx -y @upstash/context7-mcp
claude mcp add --transport stdio context-mode   -- npx -y context-mode
claude mcp add --transport stdio token-savior   -- uvx token-savior-recall
```

Install `code-review-graph` (Tree-sitter knowledge graph — run once per repo):

```bash
uv tool install code-review-graph
code-review-graph install --platform claude-code   # run inside your project
code-review-graph build
```

Servers requiring API keys (configure manually after adding):

```bash
claude mcp add --transport stdio 2slides     -- npx -y mcp-2slides
claude mcp add --transport http  slidespeak  https://mcp.slidespeak.co/mcp
claude mcp add --transport http  plusai      https://mcp.plusai.com/
claude mcp add --transport http  CustomerIO  https://mcp.customer.io/mcp
```

---

## Keep skills up to date

Run this inside the repo to pull the latest skills from all source repos:

```bash
bash sync-listed-sources.sh
```

Then commit the result:

```bash
git add skills/ skills-manifest.txt skills-source-map.tsv
git commit -m "chore: sync skills $(date +%Y-%m-%d)"
git push
```

---

## How it works

```
sync-listed-sources.sh
  ↓ clones / zip-downloads each source repo
  ↓ discovers all SKILL.md directories
  ↓ first-source-wins deduplication
  ↓ removes untrusted skills (SKIP_SKILLS list)
  ↓ writes skills/   skills-manifest.txt   skills-source-map.tsv
```

- **Precedence**: when two repos define the same skill name, the repo listed earlier in `SOURCE_INPUTS` wins.
- **Exclusions**: skills in `SKIP_SKILLS` are removed after sync (currently: `agent-browser` — Snyk High Risk flag).
- **Traceability**: every skill in `skills/` has a matching row in `skills-source-map.tsv` showing its origin repo and discovery source.

---

## Contributing

To add a new skill source:

1. Open `sync-listed-sources.sh`
2. Add a line to `SOURCE_INPUTS`:
   ```python
   {"kind": "repo", "repo": "owner/repo-name"},
   ```
3. Run `bash sync-listed-sources.sh` to pull and sync
4. Open a PR with the updated `skills/`, `skills-manifest.txt`, and `skills-source-map.tsv`

To flag a skill as unsafe, add its name to `SKIP_SKILLS` in `sync-listed-sources.sh` with a comment explaining why.
