---
name: icpg
description: Intent-Augmented Code Property Graph — tracks WHY code exists via ReasonNodes with formal contracts, 6-dimension drift detection, and 3 canonical pre-task queries for autonomous development
when-to-use: "Before any code change — query the reason graph for intent, constraints, and risk"
user-invocable: false
effort: high
---

# iCPG Skill (Intent-Augmented Code Property Graph)


**Purpose:** Add a Reason Graph layer on top of code structure so every
function, class, and module is traceable to the goal that created it,
the agent or human that owns it, and whether it's still doing what it
was supposed to do.

```
┌────────────────────────────────────────────────────────────────┐
│  iCPG = AST + CFG + PDG + RG (Reason Graph)                    │
│  ─────────────────────────────────────────────────────────────│
│  AST  = Abstract Syntax Tree (structure)      ← existing       │
│  CFG  = Control Flow Graph (execution paths)  ← existing       │
│  PDG  = Program Dependency Graph              ← existing       │
│  RG   = Reason Graph (WHY layer)              ← THIS SKILL     │
│                                                                │
│  The RG stores ReasonNodes (goals/tasks), links them to code   │
│  symbols via typed edges, enforces contracts (DbC), and        │
│  detects when code drifts from its original purpose.           │
│                                                                │
│  Storage: .icpg/reason.db (SQLite, per-project, gitignored)   │
│  CLI: icpg init | create | record | query | drift | bootstrap │
└────────────────────────────────────────────────────────────────┘
```

---

## Core Principle

**Intent first, code second.** Before writing or modifying code, query
the reason graph to understand WHY existing code was written, WHAT
constraints it must preserve, and WHETHER your change duplicates prior
work.

---

## The 3 Canonical Pre-Task Queries

**Every agent MUST run these before writing code:**

| # | Query | Command | What It Answers |
|---|-------|---------|-----------------|
| 1 | **search_prior_work** | `icpg query prior "<goal>"` | Has this been attempted before? Prevents duplication. |
| 2 | **get_constraints** | `icpg query constraints <file>` | What invariants apply to files I'll touch? Prevents breakage. |
| 3 | **get_risk_profile** | `icpg query risk <symbol>` | Is this symbol fragile? Drift history, ownership changes. |

---

## ReasonNode — The Core Primitive

Each ReasonNode captures a stated purpose with a formal contract:

```
id              UUID
goal            Natural language: what is this trying to achieve
decision_type   business_goal | arch_decision | task | workaround | constraint | patch
scope           Files/modules expected to be touched
owner           Human or agent accountable
status          proposed | executing | fulfilled | drifted | abandoned
source          manual | commit | inferred | agent-session

FORMAL CONTRACT (Design by Contract):
  preconditions    What must be true before this intent executes
  postconditions   What must be true when fulfilled
  invariants       What must remain true throughout and after
```

**Drift = predicate failure.** A symbol has drifted when its current
behavior no longer satisfies the postconditions of the ReasonNode that
created it, or when an invariant is violated.

---

## Six Edge Types

```
CREATES      Reason  → Symbol   (this intent created this function)
MODIFIES     Reason  → Symbol   (this intent changed this function)
REQUIRES     Reason  → Reason   (B depends on A being done first)
DUPLICATES   Reason  → Reason   (these two goals overlap)
VALIDATED_BY Reason  → Test     (this test proves the intent was satisfied)
DRIFTS_FROM  Symbol  → Reason   (this symbol no longer does what it was made for)
```

---

## 6-Dimension Drift Model

| Dimension | What It Means | Detection |
|-----------|--------------|-----------|
| **Spec drift** | Symbol checksum changed without a MODIFIES edge | Compare stored vs current checksum |
| **Decision drift** | Postconditions no longer hold | Evaluate predicates against codebase |
| **Ownership drift** | >3 different owners without coherent oversight | Count unique owners on edges |
| **Test drift** | VALIDATED_BY tests missing or failing | Check test file existence + run |
| **Usage drift** | Symbol used outside original scope | Grep for imports beyond scope |
| **Dependency drift** | Downstream REQUIRES reasons have drifted | Traverse REQUIRES edges |

Run `icpg drift check` to scan all dimensions. Each produces a 0-1 severity score.

---

## CLI Reference

### Setup
```bash
icpg init                          # Create .icpg/ and database
icpg bootstrap --days 90           # Infer ReasonNodes from git history
icpg bootstrap --days 90 --no-llm  # Without LLM (commit-message only)
```

### Create & Record
```bash
icpg create "Add JWT auth" --scope src/auth/ --owner feature-auth --type task
icpg record --reason <id> --base main         # Record symbols from git diff
icpg record --reason <id> --edge-type MODIFIES # Record as modifications
```

### Query (the 3 canonical queries)
```bash
icpg query prior "user authentication"     # 1. Duplicate detection
icpg query constraints src/auth/service.ts  # 2. Invariants for file
icpg query risk validateToken              # 3. Symbol risk profile
icpg query context src/auth/service.ts     # All intents for a file
icpg query blast <reason-id>               # Full blast radius
```

### Drift
```bash
icpg drift check          # Full scan across all dimensions
icpg drift resolve <id>   # Mark drift event resolved
```

### Status
```bash
icpg status               # Stats: reasons, symbols, edges, drift
```

---

## Storage

Per-project, gitignored, zero infrastructure:

```
.icpg/
  reason.db       SQLite database (4 tables: reasons, symbols, edges, drift_events)
  .gitignore      Contains: *
  chroma/         ChromaDB vectors (if chromadb installed)
  tfidf_cache.json  TF-IDF fallback cache
  .current-intent   Marker file for active intent (used by Stop hook)
```

Install options:
```bash
pip install ./scripts/icpg            # Core (zero deps)
pip install "./scripts/icpg[vectors]"  # + ChromaDB for duplicate detection
pip install "./scripts/icpg[all]"      # + ChromaDB + scikit-learn + openai
```

---

## Workflow: Before Any Code Change

```
0. INTENT       → icpg create (or identify existing intent)
1. DEDUP        → icpg query prior (check for duplicate work)
2. CONSTRAINTS  → icpg query constraints (understand invariants)
3. RISK         → icpg query risk (check fragile symbols)
4. LOCATE       → search_graph to find symbols (code-graph skill)
5. CHANGE       → Make the edit (PreToolUse hook shows context)
6. RECORD       → icpg record (link symbols to intent)
7. DRIFT CHECK  → icpg drift check (verify no unintended drift)
8. VERIFY       → Run tests, lint, typecheck
```

**Step 0 is non-negotiable for autonomous agents.** Every change must
be linked to a stated purpose. Without an intent, there's nothing to
measure drift against.

---

## Hook Integration

### PreToolUse Hook (automatic context injection)

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "scripts/icpg-pre-edit.sh",
        "timeout": 3,
        "statusMessage": "Checking intent context..."
      }]
    }]
  }
}
```

Before every file edit, agents see:
```
═══ iCPG CONTEXT ═══
INTENTS for src/auth/service.ts:
  [>] a1b2c3d4 — User authentication with JWT tokens
      Owner: feature-auth | Status: executing
      Invariants: 2
CONSTRAINTS for src/auth/service.ts:
  From intent: User authentication with JWT tokens
    INV: file_exists("src/auth/middleware.ts")
    POST: test_exists("src/auth/__tests__/service.test.ts")
PRESERVE function signatures unless your task requires changing them.
═══════════════════
```

### Stop Hook (automatic symbol recording)

After implementation passes tests, auto-records symbols:
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {"type": "command", "command": "scripts/tdd-loop-check.sh", "timeout": 60},
        {"type": "command", "command": "scripts/icpg-stop-record.sh", "timeout": 5}
      ]
    }]
  }
}
```

---

## Agent Teams Integration

### Updated Pipeline (agent-teams + iCPG)

```
 0. INTENT       Team lead creates ReasonNode from feature spec
 0b. DEDUP       icpg query prior — check for duplicate intents
 1. SPEC         Feature agent writes spec
 2. SPEC-REVIEW  Quality agent reviews spec + intent alignment
 3. TESTS (RED)  Feature agent writes tests
 4. RED-VERIFY   Quality agent verifies tests fail
 5. IMPLEMENT    Feature agent codes (PreEdit hook shows context)
 5b. RECORD      Auto-record symbols → intent (Stop hook)
 5c. DRIFT-CHECK Quality agent verifies no scope drift
 6. GREEN-VERIFY Quality agent verifies tests pass + coverage
 7. VALIDATE     Lint + typecheck + full suite
 8. CODE-REVIEW  Review agent (sees intent context per file)
 9. SECURITY     Security agent
10. BRANCH-PR    Merger agent (PR includes intent traceability)
```

### Agent Responsibilities

| Agent | iCPG Action |
|-------|-------------|
| **Team Lead** | `icpg create` when creating task chains. `icpg query prior` to check duplicates. |
| **Feature Agent** | `icpg query constraints` before implementing. Writes `.icpg/.current-intent` for auto-recording. |
| **Quality Agent** | `icpg drift check` during GREEN verify. Verifies scope alignment. |
| **Review Agent** | Sees intent context via PreToolUse hook when reviewing files. |
| **Merger Agent** | Includes intent traceability in PR description. |

---

## Bootstrapping from Git History

For existing codebases, infer ReasonNodes from commit history:

```bash
icpg bootstrap --days 90 --verbose
```

This will:
1. Get commits from last 90 days
2. Cluster by temporal proximity (2-hour window)
3. Infer intent via LLM (Claude or OpenAI) or commit message parsing
4. Create ReasonNodes with `source: "inferred"`, `confidence: 0.6-0.8`
5. Extract symbols from changed files, create CREATES edges
6. Run duplicate detection against existing ReasonNodes

**Quality note:** Inferred intents are marked low-confidence. Review and
promote high-value ones manually.

---

## Contract Predicates

Predicates are structured assertions over codebase state:

```
file_exists("src/auth/middleware.ts")
test_exists("src/auth/__tests__/service.test.ts")
symbol_count("src/auth/") <= 15
function_signature("validateToken") == "(token: string) => Promise<User>"
```

Contracts can be:
- **Hand-authored** for high-risk ReasonNodes
- **LLM-inferred** via `icpg create --infer-contracts`
- **Heuristic** (scope → file_exists, test → test_exists)

---

## Anti-Patterns

| Anti-Pattern | Do This Instead |
|-------------|-----------------|
| Coding without stating intent | `icpg create` before every non-trivial change |
| Assuming your change is isolated | `icpg query constraints` + `icpg query risk` first |
| Rebuilding what already exists | `icpg query prior` to check for prior work |
| Leaving intent in 'executing' forever | Update status to 'fulfilled' when done |
| Ignoring drift events | `icpg drift check` weekly, resolve or create new intents |
| Storing full source in symbols | Store signature + checksum only — read source from files |
| Skipping bootstrap on existing repos | `icpg bootstrap --days 90` to build initial graph |
