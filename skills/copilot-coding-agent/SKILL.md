---
name: copilot-coding-agent
description: "Use GitHub Copilot's coding agent (cloud + IDE) to autonomously implement issues end-to-end — assign Copilot, watch it open a PR, review, iterate. Covers cloud agent (no IDE needed), VS Code agent mode for local app building, and parallel task delegation. Trigger when the user mentions Copilot agent, assigning issues to Copilot, Copilot agent mode, expanding the team with Copilot, autonomous coding agent. Sourced from github.com/skills/expand-your-team-with-copilot + build-applications-w-copilot-agent-mode."
---

# GitHub Copilot Coding Agent

Copilot now ships in two agentic modes:
- **Cloud agent** — assign an issue to `@copilot`, it spins up a Codespace, implements, opens a PR. No local IDE needed.
- **VS Code agent mode** — drives the editor: creates files, runs commands, iterates on your machine.

Requires a paid Copilot subscription (Pro or higher / Business / Enterprise) and the org admin to enable it on the repo.

## Cloud Agent — Assign an Issue, Get a PR

Enable at **Repo Settings → Copilot → Coding agent → Enable**.

Once enabled, assign issues like you'd assign a teammate:
```bash
gh issue edit 42 --add-assignee Copilot
```

Or in the GitHub UI: assignee picker → Copilot. The agent:
1. Reads the issue body, comments, linked discussions
2. Spins up an ephemeral Codespace (uses your `.devcontainer/devcontainer.json` if present)
3. Explores the codebase, writes code, runs tests
4. Opens a PR linked back to the issue
5. Posts progress as PR comments

You review the PR like any human's. Ask for changes via PR review comments — the agent picks them up and pushes again. Approve and merge when good.

### What it does well
- Small-to-medium issues with a clear acceptance criterion
- Repetitive refactors (renames, library migrations)
- Bug fixes where the failing case is described
- Documentation
- Test additions when the code is already there

### What it doesn't
- Vague issues ("make it faster") — be specific
- Architecture decisions
- Cross-repo changes
- Changes that need running real external services beyond what the devcontainer provides

### Make it succeed
- **Add a `.github/copilot-instructions.md`** — see [copilot-custom-instructions](../copilot-custom-instructions/SKILL.md). Without it, the agent guesses your conventions.
- **Set up `.devcontainer/devcontainer.json`** — gives the agent a working environment immediately. Without it, the agent installs deps from scratch each time.
- **Write issues like specs** — acceptance criteria, file pointers, expected interface. Example:
  ```
  Add a /api/health endpoint that returns 200 with {status: "ok", uptime: <seconds>}.
  Implement in app/api/health/route.ts using the existing Server Action pattern.
  Add a Vitest in tests/api/health.test.ts covering 200 OK and content-type.
  ```
- **Use environment secrets** — `Settings → Codespaces → Secrets` — so the agent has API keys it needs.

## Parallel Tasks

Assign multiple issues at once. The agent works on each in its own Codespace, in parallel. Practical limit: 5-10 concurrent without conflicts. Watch out for:
- PRs that touch the same files — merge conflicts
- Dependent issues — assign in order

Use labels like `agent-ready` to mark which issues are well-scoped for autonomous work.

## VS Code Agent Mode (Local)

Different mode, same agent personality. Open Copilot Chat, switch to "Agent" mode from the dropdown, give it a multi-step task:

> Build a Next.js app for tracking gym workouts. SQLite via Drizzle. Routes for log workout, list workouts, edit. Tailwind UI. Tests with Vitest.

The agent:
1. Plans the implementation steps
2. Creates files
3. Runs `npm install` / migrations / tests
4. Reports back, asks for confirmation on big decisions
5. Iterates when you say "the form is missing validation"

### Tips for agent mode
- Start with a clear, multi-paragraph spec. The agent does best when given the destination.
- Approve commands carefully — it asks before running `rm`, `git push`, schema migrations.
- New chat for new feature — resets context, keeps it focused.
- Try different models. GPT-4o vs Claude vs Gemini handle different task shapes — switch when output stalls.

## Custom Agents

Beyond the default agent, define purpose-specific ones via `.github/agents/<name>.agent.md`:

```markdown
---
description: "Database migration writer"
tools: ["codebase", "terminal"]
model: "Claude Sonnet 4"
---

You write Drizzle migrations. For every task:
1. Read the current schema in `db/schema.ts`
2. Generate the migration via `npm run db:generate`
3. Verify the up/down SQL looks correct
4. Run `npm run db:push` against a local Postgres to verify it applies cleanly
5. Stop and ask before doing anything else

Never modify existing migration files — only add new ones.
```

Invoke via the agent picker. Useful when you want a hyper-focused agent for one job.

## Reviewing Agent Output

Treat agent PRs like junior dev PRs:
- Read the diff, not just the description
- Run the tests yourself locally if it's a meaningful change
- Push back on shortcuts — the agent will happily comment-out a failing test to "fix" it
- Check for unrelated changes — sometimes it cleans up other files; revert those if you want a focused PR

## Cost / Limits

- Agent runs consume Copilot premium request budget (varies by plan)
- Each issue assignment spins up a Codespace — Codespaces minutes apply
- Larger orgs get bulk discounts; small teams should monitor billing the first month

## Anti-Patterns

- ❌ Assigning vague issues — agent picks the easiest interpretation, often wrong.
- ❌ No `.devcontainer` — agent reinvents the dev environment every time.
- ❌ No `copilot-instructions.md` — agent doesn't know your stack.
- ❌ Merging agent PRs without reading the diff.
- ❌ Assigning a security-sensitive issue (auth, payments) without extra scrutiny.
- ❌ Treating "no failing test" as "task done" — the agent may have weakened a test rather than fix the bug.

## Quick Checklist

- [ ] Coding agent enabled in repo settings
- [ ] `.github/copilot-instructions.md` describes the stack and conventions
- [ ] `.devcontainer/devcontainer.json` provides a working env
- [ ] Codespaces secrets configured for any required env vars
- [ ] Issue template guides authors to spec out acceptance criteria
- [ ] PR review process treats agent PRs same as human PRs

## References

- Source courses: https://github.com/skills/expand-your-team-with-copilot, https://github.com/skills/build-applications-w-copilot-agent-mode
- Coding agent docs: https://docs.github.com/en/copilot/using-github-copilot/coding-agent
- Agent mode (VS Code): https://code.visualstudio.com/docs/copilot/copilot-edits
