---
name: copilot-custom-instructions
description: "Configure GitHub Copilot per-repo with custom instructions, reusable prompt files, and custom chat modes — so Copilot follows your project's conventions, frameworks, and style. Trigger when the user mentions Copilot custom instructions, .github/copilot-instructions.md, Copilot prompt files, custom chat modes, agent skills, or tailoring Copilot to a codebase. Sourced from github.com/skills/customize-your-github-copilot-experience."
---

# Customize GitHub Copilot

Out-of-the-box Copilot has no idea your team uses Drizzle ORM, your auth lives in `lib/session.ts`, or that comments must be sentence-case. Custom instructions, prompts, and chat modes tell it. The payoff is dramatic — generated code that fits the codebase on the first attempt.

## Three Levels

| Mechanism | Scope | When loaded |
|---|---|---|
| **Repo instructions** (`.github/copilot-instructions.md`) | All Copilot interactions in the repo | Automatically, every request |
| **Path-scoped instructions** (`.github/instructions/*.instructions.md`) | Files matching a glob | When you edit a matching file |
| **Prompt files** (`.github/prompts/*.prompt.md`) | Ad-hoc, manually invoked | When you run `/<name>` in Chat |
| **Custom chat modes** (`.github/chatmodes/*.chatmode.md`) | Whole Chat session | When you switch mode in the picker |

## Repo-Wide Instructions

`.github/copilot-instructions.md` — the "everything Copilot needs to know about this repo" file. Keep it under ~200 lines; Copilot's context budget is finite.

Example:
```markdown
# Project: Acme Dashboard

## Stack
- Next.js 15 App Router + React 19
- TypeScript strict mode
- Drizzle ORM + Postgres (Neon)
- Auth: better-auth in lib/auth.ts
- UI: shadcn/ui + Tailwind v4
- Tests: Vitest + Playwright

## Conventions
- Server components by default; mark `"use client"` only when needed
- Server Actions for mutations, no API routes for CRUD
- Drizzle queries colocated in `app/<feature>/queries.ts`
- Component files use named exports, not default
- File naming: kebab-case for files, PascalCase for components

## Style
- Sentence-case in comments and copy
- No emojis in code
- Prefer `??` over `||` for default fallbacks
- Error handling: throw typed errors from `lib/errors.ts`, never plain strings

## Don't
- No `any` types. Use `unknown` and narrow.
- No console.log in committed code.
- No client-side fetch to internal APIs — call Server Actions or queries directly.
```

The clearer and more specific, the better the output. Avoid platitudes ("write good code"). Pin down what's nonobvious.

## Path-Scoped Instructions

For framework- or directory-specific guidance, put it next to the code:

`.github/instructions/sql.instructions.md`:
```markdown
---
applyTo: "**/*.sql,**/migrations/**"
---
- Use snake_case for table and column names
- Every table needs `id uuid primary key default gen_random_uuid()` and `created_at timestamptz default now()`
- Never use `select *` in application queries
- Migrations are append-only — never edit existing migration files
```

`.github/instructions/components.instructions.md`:
```markdown
---
applyTo: "components/**/*.tsx"
---
- Named exports only, never default
- Props interfaces named `<Component>Props`
- forwardRef when component renders a DOM node
- Use cva() for variant styles (see button.tsx for pattern)
```

The `applyTo` frontmatter is glob-matched. When editing a matching file, these instructions stack on top of the repo-wide ones.

## Prompt Files (Reusable Slash Commands)

For repetitive tasks — scaffolding, refactors, audits.

`.github/prompts/add-feature.prompt.md`:
```markdown
---
description: "Scaffold a new feature directory with route, query, and component"
mode: "agent"
---

Scaffold a new feature called `{{featureName}}`.

Create these files:
1. `app/{{featureName}}/page.tsx` — Server component, renders `<FeatureName>` from queries.ts
2. `app/{{featureName}}/queries.ts` — Drizzle query named `get{{FeatureName}}List(userId: string)`
3. `app/{{featureName}}/actions.ts` — Server Action `create{{FeatureName}}` with Zod validation
4. `components/{{featureName}}/feature-name-list.tsx` — Renders the list

Reference patterns from `app/projects/` — match style.
```

Invoke in Chat: `/add-feature billing`. Variables in `{{}}` get filled by the model from your prompt.

`.github/prompts/audit-perf.prompt.md`:
```markdown
---
description: "Audit a route for client-side performance issues"
mode: "agent"
---

Audit `${file}` for:
- Unnecessary "use client" — should this be server?
- N+1 queries in loops
- Unbounded list rendering without virtualization
- Heavy imports that should be dynamic
- Missing React.memo / useMemo on expensive renders

Report findings with file:line. Suggest fixes, don't apply them.
```

## Custom Chat Modes

Whole-session personas. Useful when the same conversation style applies for an extended task.

`.github/chatmodes/security-review.chatmode.md`:
```markdown
---
description: "Security-focused code review"
tools: ["codebase", "search"]
model: "Claude Sonnet 4"
---

You are reviewing this codebase for security issues. For every file or change you look at:
1. Check for unsanitized user input reaching SQL, HTML, shell, or filesystem APIs
2. Check authentication/authorization on every mutation
3. Check for secrets in code, logs, or error messages
4. Flag deprecated crypto (md5, sha1, des, ecb)

Report findings as `LOC | severity | issue | suggested fix`. No code generation — only review.
```

Switch to it via the mode picker in Copilot Chat. Subsequent messages in the session use these instructions.

## What Goes Where

| Type of guidance | Put it in |
|---|---|
| Stack, conventions, project structure | `copilot-instructions.md` |
| Language- or directory-specific rules | `instructions/*.instructions.md` (with `applyTo`) |
| Repetitive tasks (scaffolds, audits) | `prompts/*.prompt.md` |
| Distinct workflows (review mode, docs mode) | `chatmodes/*.chatmode.md` |
| API keys, secrets | Nowhere — use Codespaces/repo secrets |

## Validating

After authoring instructions, test in Chat:
- Ask Copilot something where the instructions should kick in
- Inspect the response — does it follow the conventions you wrote down?
- If not: the instructions are too vague, too long, or contradictory. Shorten and sharpen.

GitHub also offers a "References" view in Chat showing which instructions/prompts were included for a given response.

## Anti-Patterns

- ❌ 1000-line `copilot-instructions.md` — context cost is real; it crowds out the actual code.
- ❌ "Write clean code" without specifying what clean means in this repo.
- ❌ Path-scoped instructions with overlapping globs and contradictions.
- ❌ Prompt files that hardcode user names, dates, or session-specific values.
- ❌ Storing real secrets in any of these files.
- ❌ Forgetting that these files are public if the repo is public — don't reveal internal architecture you wouldn't share otherwise.

## Quick Checklist

- [ ] `.github/copilot-instructions.md` exists and is under 200 lines
- [ ] Path-scoped instructions for language/directory-specific rules
- [ ] At least 2-3 prompt files for repetitive scaffolding
- [ ] Custom chat modes for distinct workflows (review, docs, refactor)
- [ ] Tested by asking Copilot a question where instructions apply
- [ ] No secrets or internal-only details in committed instruction files

## References

- Source course: https://github.com/skills/customize-your-github-copilot-experience
- Custom instructions docs: https://docs.github.com/en/copilot/customizing-copilot/about-customizing-github-copilot-chat-responses
- Prompt files: https://docs.github.com/en/copilot/customizing-copilot/adding-personal-custom-instructions-for-github-copilot
