---
name: copilot-spaces
description: "Use GitHub Copilot Spaces to scale institutional knowledge — bundle repos, docs, transcripts, and notes into a curated context that Copilot can reason over and your team can share. Trigger when the user mentions Copilot Spaces, institutional knowledge, knowledge base for Copilot, sharing Copilot context with team, onboarding via Copilot, or 'organize what Copilot knows.' Sourced from github.com/skills/scale-institutional-knowledge-using-copilot-spaces."
---

# GitHub Copilot Spaces

A Space is a curated context bundle: code, PRs, issues, free-text notes, transcripts, images, files. You ask questions against the Space; Copilot grounds answers in only that context. Share the Space with your team so everyone gets the same expert.

Compared to repo-wide custom instructions (always-on, applies to every interaction): Spaces are **on-demand contexts**, swappable, shareable, with richer source types.

## When a Space Beats Other Approaches

| Situation | Best tool |
|---|---|
| "Always follow these conventions when editing this repo" | `.github/copilot-instructions.md` |
| "Onboard a new hire to our payments module" | Copilot Space |
| "Look across 4 repos + design docs + meeting notes to answer this" | Copilot Space |
| "Quick one-off question about a public library" | Default Copilot Chat |
| "Capture how we run incident response" | Copilot Space |
| "Generate code following our repo conventions" | Custom instructions + Chat |

Spaces shine for **multi-source knowledge that crosses repos, lives partly outside code, and is read more often than it changes**.

## Anatomy of a Space

Create at https://github.com/copilot/spaces.

Sources you can add:
- **Repositories** — entire repo or specific paths/branches
- **Files** — individual files from any repo
- **Pull requests** — for "how did we ship this feature" context
- **Issues** — for "what known issues exist around X"
- **Free-text content** — paste meeting notes, transcripts, design docs, decision records
- **Image uploads** — diagrams, screenshots, whiteboard photos
- **File uploads** — PDFs, slides, CSVs

Instructions field — a paragraph telling Copilot how to interpret the sources. Treat it like a system prompt for this Space.

Sources auto-sync. If you add a repo, file changes there flow into the Space on next query. Spaces stay live.

## Example: Onboarding Space

**Name:** `Onboarding — Payments`

**Instructions:**
> You help new engineers on the payments team. Use the included repos and docs to answer. When showing code, link to specific files. When uncertain, suggest who to ask (names are in the Team Roster doc).

**Sources:**
- Repo: `payments-api` (main branch)
- Repo: `payments-worker` (main branch)
- File: `docs/architecture/payments-overview.md` from `engineering-docs`
- Free text: Team roster (pasted)
- Free text: Common gotchas (pasted)
- PR: #1247 "Stripe webhook hardening" (a representative example of a typical PR)
- Issue: #890 "Idempotency key collisions" (representative bug)

Share with the team. New hires open the Space, ask questions like "where do we handle Stripe webhook retries?" — Copilot answers with grounded references.

## Example: Project Management Space

**Name:** `Q1 Roadmap`

**Instructions:**
> You help track Q1 commitments. Reference issues, PRs, and the roadmap doc. When asked for status, summarize from the linked issues. Flag dates that are slipping.

**Sources:**
- Issues: filter for label `q1-2026`
- PRs: filter for milestone `Q1 Launch`
- Free text: The roadmap doc
- Free text: Last 3 weekly status updates

Use it for standups, exec updates, retrospectives.

## Example: Incident Response Space

**Name:** `Incident Playbook`

**Instructions:**
> You're an incident commander. When the user says "incident: X", walk through our SEV scoring rubric, suggest first 5 minutes actions per our runbook, point to the right Slack channels, and pull relevant past incident postmortems if X resembles them.

**Sources:**
- Free text: SEV rubric, decision tree
- Free text: First-5 actions checklist
- File: All `incidents/*.md` postmortems from `engineering-docs`
- Free text: On-call rotation contact info

When something breaks, open the Space, type the symptom — get a structured response.

## Creating Issues from a Space

The Space UI has a "Create issue" button. Useful when a conversation surfaces work that needs tracking. The created issue is linked back to the Space and inherits relevant context.

## Sharing

Spaces can be:
- **Private** — only you
- **Shared with org/team** — anyone in scope can use it
- **Public** within the org — discoverable in the Spaces directory

For onboarding, share broadly. For sensitive context (acquisition planning, security incidents), keep private and grant explicitly.

## Authoring Tips

- **Tight scope wins.** A focused Space outperforms a kitchen-sink one. Multiple narrow Spaces > one giant Space.
- **Curate, don't dump.** A 300-line free-text "everything important about payments" is worse than 5 well-chosen sources.
- **Update instructions when the team grows.** "Suggest who to ask" only works if the roster is current.
- **Review quarterly.** Stale source files create confidently wrong answers.
- **Add representative examples.** A "good PR" and a "bad PR" linked to the Space teaches more than rules.

## Anti-Patterns

- ❌ Adding 20 repos to a Space "just in case" — Copilot's context budget spreads thin, answers degrade.
- ❌ Pasting a 50,000-token document as free text — split it into focused chunks across sources.
- ❌ Treating a Space as docs — if everything is in the Space and nothing in the repo, new hires can't grep.
- ❌ Letting Spaces drift — file lists change, owners leave, conventions update.
- ❌ Sharing a Space with sensitive PR/issue references org-wide without realizing.
- ❌ Using a Space as a substitute for custom instructions in repos you own.

## Quick Setup Checklist

- [ ] Created Space with clear name reflecting purpose
- [ ] Instructions field describes how to interpret sources
- [ ] Sources are curated (3-10 typical), not dumped
- [ ] Visibility set correctly (private / team / org-wide)
- [ ] At least one representative example (good PR, model issue) included
- [ ] Quarterly calendar reminder to review and prune

## References

- Source course: https://github.com/skills/scale-institutional-knowledge-using-copilot-spaces
- Copilot Spaces docs: https://docs.github.com/en/copilot/using-github-copilot/copilot-spaces
- Spaces hub: https://github.com/copilot/spaces
