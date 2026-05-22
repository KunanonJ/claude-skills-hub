---
name: large-codebase-codex
description: Use when navigating, onboarding, planning, or safely changing a large or unfamiliar codebase, including monorepos, legacy systems, multi-service repos, multi-repo architectures, repo maps, AGENTS.md/project-context setup, scoped verification, subagent exploration, MCP/LSP setup decisions, or Codex adoption workflows for engineering teams.
---

# Large Codebase Codex

Use this skill to make a large repo legible before editing. It adapts the patterns from Anthropic's large-codebase guidance for Codex: live codebase search, lean layered context, on-demand skills, scoped verification, symbol-aware navigation where available, and separating exploration from edits.

Source basis: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start

## Core Principles

- Prefer live repo evidence over stale memory or assumed indexes: inspect the current checkout with `git`, `rg`, `rg --files`, project docs, package/workspace config, and existing tests.
- Do not bulk-read the repo. Build a map, form a hypothesis, then open only the files needed.
- Keep persistent context lean. Broad repo facts belong in root `AGENTS.md`; local conventions belong in subdirectory `AGENTS.md`; reusable task expertise belongs in a skill.
- Scope work to the relevant subdirectory when possible, while preserving awareness of root-level tooling and shared libraries.
- Use deterministic checks for deterministic rules: lint, formatting, typecheck, tests, build, schema checks, or project-specific scripts.
- Split exploration from editing when the repo is wide. Read-only subagents can map areas; the main agent should consolidate and make edits.

## Workflow

### 1. Anchor the Task

Before changing files:

- Confirm the requested behavior or question in one sentence.
- Check `pwd`, `git status --short --branch`, and the current branch.
- Identify whether the task is read-only, a behavior change, a refactor, or a repo-setup task.
- Classify risk: docs/context is usually low risk; public APIs, schema, auth, payments, production data, deploys, and force pushes are higher risk.

If the user asks for a change, preserve unrelated local changes. Never reset or checkout over user work.

### 2. Build a Repo Map

Start broad, then narrow:

```bash
rg --files -g 'AGENTS.md' -g 'README*' -g 'package.json' -g 'pnpm-workspace.yaml' -g 'turbo.json' -g 'pyproject.toml' -g 'go.mod' -g 'Cargo.toml'
rg --files | sed 's#/.*##' | sort | uniq -c | sort -nr | sed -n '1,40p'
```

Read only the relevant root docs and config first. Look for:

- Top-level product/module boundaries.
- Ownership or package/workspace structure.
- Test, lint, typecheck, and build commands.
- Generated, vendored, build, or third-party directories to avoid.
- Existing local instructions in `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, docs, or package scripts.

If the directory structure is unclear, create an ephemeral map in your working notes. Only add a tracked `docs/CODEBASE_MAP.md` or `AGENTS.md` update when the user requested repo setup or the repeated confusion is material to the task.

### 3. Locate the Relevant Slice

Use specific live searches:

```bash
rg -n "routeName|componentName|error text|functionName|GraphQLField"
rg -n "describe\\(|it\\(|test\\(" path/to/likely/package
rg --files path/to/likely/package | sed -n '1,120p'
```

Prefer symbol-aware tools when available through an IDE, LSP, language server plugin, or MCP. Use text search as the fallback, but be alert for common names that produce false matches.

For wide investigation that needs more than a few files, spawn read-only exploration subagents if available. Give each subagent a narrow area and ask for file paths, line references, and confidence. Do not let multiple agents edit overlapping files without consolidation.

### 4. Plan Before Editing

For non-trivial changes, write a compact plan:

```text
GOAL: one sentence
SCOPE IN: files/packages/flows touched
SCOPE OUT: what will not change
RISK: low/medium/high and why
STEPS: concrete edit sequence
VERIFICATION: exact commands or smoke checks
ROLLBACK: revert commit, restore file, disable flag, or config rollback
```

For behavior changes, prefer test-first work when the repo has a usable test harness. If tests cannot be added, say why and choose the smallest observable verification.

### 5. Edit in Small Slices

- Make the smallest change that satisfies the planned behavior.
- Keep refactors separate from behavior changes unless the refactor is necessary to make the behavior safe.
- Use the project's existing style, naming, and dependency patterns.
- When multiple packages are involved, edit from leaf behavior toward shared abstractions, not the other way around.
- Capture any discovered repo facts that future agents need, but do not bloat persistent docs with task-local details.

### 6. Verify with Scoped Commands First

Prefer local/scoped checks before full-suite checks:

```bash
# examples; adapt to the repo
npm test -- path/to/spec
pnpm --filter package-name test
yarn tsc --noEmit
cargo test -p crate_name
go test ./path/to/package
```

Run broader checks when:

- The change touches shared libraries, generated types, build config, or public APIs.
- Scoped tests pass but the blast radius is uncertain.
- The user asked for production readiness or "make sure everything works."

Report exact command outcomes. If a verification fails for unrelated existing debt, include the evidence and avoid claiming the change is fully verified.

## Maintaining Codex Context

When improving repo setup for Codex:

- Root `AGENTS.md`: keep only project-wide facts, top-level map, critical gotchas, core commands, and safety boundaries.
- Subdirectory `AGENTS.md`: put local commands, ownership, architecture, generated-file warnings, and package-specific pitfalls.
- Skills: create for reusable workflows such as release, migrations, security review, data imports, or design-system work.
- MCP servers: add only when Codex needs structured access to external systems or internal APIs. Do not build MCP connections before the local repo context and verification commands are usable.
- Periodic cleanup: review `AGENTS.md`, skills, MCP configs, and automation every 3-6 months or after major model/tooling changes. Remove over-specific rules that newer tooling no longer needs.

## Anti-Patterns

- Reading the whole repo before forming a hypothesis.
- Putting every convention into root `AGENTS.md`.
- Running the entire monorepo test suite as the first verification step for a one-package edit.
- Trusting stale docs over current code.
- Mixing read-only exploration, design decisions, and production edits in one unbounded pass.
- Adding MCP servers or plugins to compensate for missing basic repo maps and commands.
- Letting good setup remain tribal instead of promoting it to `AGENTS.md`, skills, scripts, or repo docs.

## Handoff Shape

End large-codebase work with:

- What changed or what was learned.
- Key files/packages touched or mapped.
- Verification commands and results.
- Remaining risks, blockers, or unverified assumptions.
- The next concrete step for a future Codex session.
