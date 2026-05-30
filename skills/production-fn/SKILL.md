---
name: production-fn
description: Write a function as if it's shipping to fintech production — full type hints, docstrings, input validation, logging, exhaustive error handling, 5+ unit tests, performance notes, and scale warnings. Use when the user asks to write a function for production use, fintech, high-stakes, payment/financial, or requests "production-ready" / "production-grade" code.
---

# Production-Grade Function

Write the function as if it's shipping into a real fintech production system. The reader is on-call and will get paged when this breaks.

**Mandatory elements:**

1. **Type hints** — complete signatures, including return types and generic parameters. No `Any` unless justified.

2. **Docstring** — purpose, args, returns, raises, examples, complexity note if non-trivial.

3. **Input validation** — at the function boundary. Clear error messages that name the offending parameter and the constraint violated. Use schema validation (Pydantic / zod / equivalent) for structured input.

4. **Logging** — appropriate levels:
   - `DEBUG`: input shape, intermediate state for tracing
   - `INFO`: meaningful state transitions (one-line, structured)
   - `WARN`: recoverable anomalies
   - `ERROR`: failures with context
   - Never log secrets, PII, or full request bodies

5. **Error handling for every failure mode**:
   - Invalid input
   - External call failure (network, timeout)
   - Partial failure (some succeed, some don't)
   - Resource exhaustion (memory, connections, rate limit)
   - Concurrency (race, deadlock, retry)
   - Unexpected (catch-all with context, then re-raise)

6. **Unit tests** — at minimum:
   - Happy path
   - Boundary values (empty, max, off-by-one)
   - Invalid input
   - External failure
   - Concurrent / re-entrant if applicable
   - Regression for any subtle case in the spec
   - Aim for ≥5 cases, more if the function has branches

7. **Performance notes** — time/space complexity, allocations in hot path, blocking I/O, expected throughput ceiling.

8. **Scale warnings** — explicit comment block: "This breaks when ___" (e.g., "input > 10k items: switch to streaming"; "concurrent calls > N: needs distributed lock").

**No shortcuts. No placeholders.** If you don't have enough context to make a real choice (e.g., which logger, which DB driver), ask before writing.
