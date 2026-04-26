---
name: gstack
description: Garry Tan's (YC CEO) virtual engineering team for Claude Code — 23+ specialist slash commands (CEO, eng manager, designer, QA, security, release engineer) that turn Claude into a full software factory. Use when asked to "use gstack", "plan a feature", "review code", "run QA", "ship a PR", or "security audit".
license: MIT
metadata:
  author: KunanonJ
  version: "1.0"
  source: https://github.com/garrytan/gstack
---

# gstack

> "I don't think I've typed like a line of code probably since December." — Andrej Karpathy, March 2026

**gstack** is [Garry Tan](https://x.com/garrytan)'s open-source software factory for Claude Code. It turns Claude into a virtual engineering team — 23+ specialists and 8 power tools as slash commands, all Markdown, MIT license.

## Install

```bash
# 30-second install
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack \
  && cd ~/.claude/skills/gstack && ./setup
```

Then add to your `CLAUDE.md`:
```markdown
## gstack
Use /browse from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.
Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /design-shotgun, /design-html, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /open-gstack-browser, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /setup-gbrain, /retro, /investigate, /document-release, /codex, /cso, /autoplan, /pair-agent, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn.
```

**Requirements:** Claude Code, Git, Bun v1.0+

## Sprint Workflow

gstack follows a **Think → Plan → Build → Review → Test → Ship → Reflect** loop:

1. `/office-hours` — Product thinking session (describe what you're building)
2. `/plan-ceo-review` — Strategic plan review (CEO lens)
3. `/plan-eng-review` — Architecture lock + implementation plan
4. `/plan-design-review` — Design direction before build
5. _(build)_
6. `/review` — Code review with bug hunting
7. `/qa` — Real browser QA on staging URL
8. `/ship` — PR creation + release notes
9. `/retro` — Session retrospective

## All Skills

### Planning & Strategy
| Skill | Purpose |
|-------|---------|
| `/office-hours` | Product thinking, refine your idea |
| `/plan-ceo-review` | CEO-lens strategic plan review |
| `/plan-eng-review` | Eng manager architecture review |
| `/plan-design-review` | Design direction review |
| `/autoplan` | Auto-generate full implementation plan |
| `/codex` | Deep research + documentation |

### Building
| Skill | Purpose |
|-------|---------|
| `/design-consultation` | Design direction conversation |
| `/design-shotgun` | Generate 3 design directions to pick from |
| `/design-html` | Build HTML/CSS from design spec |
| `/design-review` | Review UI for design quality |
| `/pair-agent` | Pair programming mode |

### Review & Quality
| Skill | Purpose |
|-------|---------|
| `/review` | Full code review (bugs, logic, security) |
| `/cso` | Chief Security Officer OWASP + STRIDE audit |
| `/qa` | Real browser QA on a URL |
| `/qa-only` | QA without build steps |
| `/investigate` | Deep investigation / root cause analysis |

### Shipping
| Skill | Purpose |
|-------|---------|
| `/ship` | Create PR + release notes |
| `/land-and-deploy` | Merge + deploy to production |
| `/canary` | Canary deploy with monitoring |
| `/document-release` | Document what shipped |
| `/benchmark` | Performance benchmarking |

### Session Control
| Skill | Purpose |
|-------|---------|
| `/careful` | Enter careful mode (confirm before actions) |
| `/freeze` | Freeze codebase (read-only) |
| `/guard` | Guard mode (protect critical files) |
| `/unfreeze` | Exit freeze/guard mode |
| `/learn` | Save key decisions and context |
| `/retro` | Session retrospective |

### Browser & Deploy
| Skill | Purpose |
|-------|---------|
| `/browse` | Headless browser for any web task |
| `/open-gstack-browser` | Open visible browser |
| `/setup-browser-cookies` | Configure auth cookies |
| `/setup-deploy` | Configure deploy pipeline |
| `/setup-gbrain` | Configure AI memory (gbrain) |
| `/gstack-upgrade` | Self-update gstack |

## Team Mode

To auto-install gstack for all teammates:

```bash
(cd ~/.claude/skills/gstack && ./setup --team) \
  && ~/.claude/skills/gstack/bin/gstack-team-init required \
  && git add .claude/ CLAUDE.md \
  && git commit -m "require gstack for AI-assisted work"
```

## Quick Start

```
/office-hours    # Describe what you're building
/plan-ceo-review # Plan the feature
/review          # Review code changes
/qa              # Test on staging
/ship            # Create the PR
```

## References

- [gstack repo](https://github.com/garrytan/gstack)
- [Garry Tan on X](https://x.com/garrytan)
- [On the LOC Controversy](https://github.com/garrytan/gstack/blob/main/docs/ON_THE_LOC_CONTROVERSY.md)
