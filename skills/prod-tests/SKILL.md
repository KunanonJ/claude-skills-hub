---
name: prod-tests
description: Write tests that catch real production bugs — edge cases from actual user behavior, race conditions, boundary values, external-dependency failures, regressions, and hot-path performance. Skip trivial happy-path assertions. Use when the user asks to write tests, improve test coverage, or test "for real" / "for production" cases.
---

# Tests That Catch Real Production Bugs

**Do not write generic happy-path tests.** Write tests that prevent the bugs that actually break production.

For the code the user shares, generate tests covering:

1. **Edge cases from real user behavior**:
   - Empty input, single element, max-size input
   - Unicode, RTL text, emoji, mixed scripts
   - Whitespace-only, null-equivalent, malformed
   - Concurrent users hitting the same resource
   - Slow clients, dropped connections

2. **Race conditions and concurrency**:
   - Two requests writing the same row
   - Read-modify-write without locking
   - Cache invalidation timing
   - Background job racing with foreground request

3. **Boundary values that break assumptions**:
   - Off-by-one at limits
   - Overflow (int, string length, array bounds)
   - Empty collections passed to "find" or "first"
   - Time around DST, leap year, year 2038, midnight UTC vs local

4. **External dependency failure modes**:
   - DB unreachable
   - DB returns partial data (timeout mid-result)
   - Third-party API rate-limits / 5xx / 4xx
   - Auth token expired during long operation
   - Disk full, file locked

5. **Regression tests for past bugs**:
   - If there are known historical bugs (git log, comments), add a test naming the bug
   - Format: `test_regression_<issue-id>_<short-description>`

6. **Performance tests for hot paths**:
   - Identify the code path that runs on every request
   - Assert latency ceiling or allocation budget
   - Mark slow tests so they can be opt-in in CI

**Skip trivial assertions.** Don't test the language itself (no "test that `+` adds"). Don't test framework behavior (no "test that decorator runs"). Test only what could plausibly break the system.

Every test should answer: "What bug does this prevent?" If the answer is "none I can think of," delete it.

Format each test with a one-line comment naming the failure mode it guards against.
