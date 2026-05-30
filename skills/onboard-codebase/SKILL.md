---
name: onboard-codebase
description: Map an unfamiliar codebase for someone joining the team — entry points, execution flow, core vs peripheral modules, conventions, safe starting points, legacy/risky areas, and questions to ask the team. Use when the user is exploring a new codebase, onboarding to a project, "where do I start", "what does this repo do", or asks for a high-level architecture explanation.
---

# Codebase Onboarding Map

The user is new to this codebase. Explain it like you would for a new hire on their first week.

Cover these areas in order:

1. **Entry points** — where execution actually starts:
   - HTTP server / API entry
   - CLI entrypoints
   - Background workers / cron jobs
   - Build/deploy entrypoints
   Trace the first 1-2 levels of the call tree from each.

2. **Core vs peripheral modules** — separate:
   - **Core**: domain logic, business rules, primary data models
   - **Plumbing**: HTTP layer, DB adapters, queue clients
   - **Peripheral**: utilities, scripts, tooling, examples
   - **Generated/vendored**: don't touch

3. **Conventions in this codebase** — read enough to find:
   - Naming patterns (files, functions, classes, tests)
   - How errors are handled
   - How config is loaded
   - How dependencies are injected
   - Testing patterns (unit colocated? separate? mocks? real deps?)
   - Logging conventions

4. **Safe places to make first changes** — areas where:
   - Tests are good
   - Surface area is small
   - Failure is loud and immediate
   Avoid: shared utilities, config, anything called from many places.

5. **Legacy / high-risk zones** — flag:
   - Code with comments like "DO NOT TOUCH", "legacy", "TODO: rewrite"
   - Modules with no tests
   - Files with high churn in git history
   - Anything with `unsafe`, `ignore`, `eslint-disable`, `# type: ignore`
   - Old patterns the rest of the codebase has moved away from

6. **Questions to ask the team** — concrete questions only the team can answer:
   - "Why does X exist? It looks duplicated with Y."
   - "Is Z module still used? It looks dead."
   - "What's the deploy/release process for this service?"
   - "Who owns the database schema?"
   - "What's the on-call expectation?"

Use the actual code structure the user provides. Don't make up file names or modules.
