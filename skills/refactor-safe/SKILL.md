---
name: refactor-safe
description: Refactor code carefully as if it's running in production. Map callers, analyze side effects, show before/after diff, identify deployment risks, and propose a safe migration path. Use when the user wants to refactor, restructure, rename, extract, or clean up code that is or might be running in production.
---

# Refactor Without Breaking Production

Treat the code the user shares as a live production system, not a side project.

Follow these steps in order:

1. **Map the call graph** — identify every function, module, route, job, or test that calls into this code. Use grep/search to verify, don't guess.
2. **Side effects and dependencies** — list every external touch: DB writes, network calls, file I/O, env vars, global state, timers, queues. Note any implicit contracts (return type expectations, error types thrown, ordering guarantees).
3. **Before/After diff** — show the exact change, side by side. No skipping "obvious" parts.
4. **Production risks** — concrete failure modes:
   - What breaks for in-flight requests during deploy?
   - What if old/new code runs simultaneously (rolling deploy)?
   - What if a cached value, queued message, or DB row was written by old code and read by new code?
   - What gets logged differently?
   - What metrics/alerts shift?
5. **Migration plan** — sequenced steps with rollback at each:
   - Feature-flag or dual-write where applicable
   - Order of merges (e.g., add new path → migrate callers → remove old path)
   - Validation between steps
   - How to revert each step

Stop and ask if anything is ambiguous before proposing the diff. A refactor that needs context you don't have is worse than no refactor.

The goal isn't "cleaner code." The goal is "still works correctly, users unaffected, reversible."
