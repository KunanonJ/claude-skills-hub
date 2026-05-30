---
name: perf-detective
description: Diagnose performance problems before optimizing — identify the bottleneck (CPU/memory/I/O/network), compute time complexity, flag allocations, detect N+1 / repeated work, predict profiler output, and rank fixes by effort vs impact. Use when the user reports slow code, latency issues, high CPU/memory, or asks to optimize / make-faster / "why is this slow".
---

# Performance Detective

**Don't optimize yet.** Diagnose first.

For the slow code the user shares, work through this analysis in order:

1. **Bottleneck classification** — which resource is constrained?
   - **CPU**: tight loops, parsing, encoding, crypto, regex backtracking
   - **Memory**: large allocations, copies, retained references, GC pressure
   - **I/O**: disk reads/writes, file scans
   - **Network**: round-trips, payload size, DNS, TLS handshake
   - If you can't tell from the code alone, **say so** and ask what's been measured.

2. **Time complexity** — best case, average, worst case. Specifically:
   - What is the dominant operation?
   - What input shape triggers worst case?
   - At what input size does it stop being acceptable?

3. **Allocation map** — where does memory get allocated?
   - Inside hot loops? (red flag)
   - Per-request? Per-element?
   - Are there obvious reuses (buffer pooling, slice growth) being missed?

4. **N+1 and repeated computation**:
   - Database: query per row instead of single query with join/IN
   - Cache: cache miss for value that didn't change
   - Computed property called repeatedly in a loop
   - Memoization opportunities

5. **Predicted profiler output** — if a profiler ran, what would be at the top?
   - Function names you'd expect to dominate
   - Where you'd be surprised to see time
   - What sampling vs allocation profile would each reveal differently

6. **Fix ranking** — two columns:
   - **Easiest wins**: small change, modest improvement (e.g., extract loop invariant, add index)
   - **Highest impact**: bigger change, large improvement (e.g., batch the API, switch algorithm)
   Recommend the easiest-win-with-meaningful-impact first.

Only after this analysis, propose the fix. If measurements would change the diagnosis, say "measure first, here's what to instrument."

**Diagnose before you prescribe.**
