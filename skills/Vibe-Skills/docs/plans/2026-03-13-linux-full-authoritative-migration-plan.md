# Linux Full-Authoritative Migration Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Linux a real `full-authoritative` runtime lane through project-side adaptation, without weakening the current Windows authority lane or causing any functional regression.

**Architecture:** The migration must not be a documentation-only promotion. The core move is to extract the current PowerShell-only authoritative checks into a runtime-neutral core, then keep `ps1` and `sh` as thin wrappers over the same semantics. Windows remains the release authority during migration, and Linux is promoted only after fresh-machine proof, parity checks, and rollback-tested evidence all pass.

**Tech Stack:** PowerShell, Bash, Python, existing `scripts/verify/*.ps1` governance gates, JSON receipts, platform adapter contracts, status/proof documentation.

---

## Context

Current repository truth is already clear:

- Windows is the only proven `full-authoritative` platform lane.
- Linux with `pwsh` is `supported-with-constraints`.
- Linux without `pwsh` is `degraded-but-supported`.
- The actual blockers are not README wording, but three PowerShell-centric authority surfaces:
  - installed runtime freshness
  - release/install/runtime coherence
  - bootstrap doctor / deep doctor

That means Linux cannot become truly full-authoritative by adding more shell glue or more documentation. The repo must first remove the **PowerShell-only authority assumption** from the authoritative path itself.

## Target Definition

Linux can be promoted to `full-authoritative` only when all of the following are true:

1. `install.sh` completes the same authoritative install validation path without requiring `pwsh`.
2. `scripts/bootstrap/one-shot-setup.sh` completes authoritative materialization and doctor preparation without falling back to warning-only skips.
3. `check.sh --profile full --deep` executes freshness, coherence, and bootstrap doctor semantics directly on Linux without `pwsh`.
4. Fresh-machine Linux runs produce the same class of receipts and governance evidence as Windows.
5. Windows remains green on the original release-authority path during and after migration.
6. Support labels are upgraded only after proof artifacts, parity gates, and rollback tests all pass.

## Non-Goals

This migration does **not** do the following:

- does not promote macOS in the same batch
- does not broaden host claims beyond what proof supports
- does not rewrite router semantics
- does not redesign the VibeSkills governance model
- does not weaken or replace PowerShell wrappers on Windows
- does not claim that every host has identical closure strength

## Hard Constraints

### Constraint 1: Windows authority is frozen

Windows remains the reference closure lane throughout the migration.

- No Linux-facing change is allowed to break `install.ps1`, `check.ps1`, or existing PowerShell governance gates.
- No public support wording is upgraded if Windows baseline turns red.

### Constraint 2: No silent degrade

If an authoritative surface is unavailable, the system must say so explicitly. It must never:

- skip a gate silently
- convert a skipped gate into an apparent success
- claim parity because wrappers exist

### Constraint 3: Runtime-neutral means semantic parity, not approximate parity

The new cross-platform core must preserve:

- gate intent
- receipt schema
- pass/fail criteria
- operator-facing error classification

If the runtime-neutral implementation changes semantics, it is a regression until proven otherwise.

### Constraint 4: Promotion is evidence-gated

Support labels in:

- `adapters/codex/platform-linux.json`
- `docs/universalization/platform-support-matrix.md`
- `docs/universalization/platform-parity-contract.md`
- `README.md`
- `README.en.md`

must not be upgraded before proof closure.

## Proof Standard

Promotion requires all of the following evidence:

1. Windows baseline pass on the current authoritative lane.
2. Linux fresh-machine pass on the runtime-neutral lane.
3. Side-by-side receipt parity between PowerShell wrappers and runtime-neutral core on Windows.
4. Linux deep check proof without `pwsh`.
5. Rollback rehearsal showing the repo can revert the promotion without breaking install/check/docs coherence.

## Workstream Overview

The migration is split into eight tasks. Tasks 1 and 2 freeze truth and design boundaries. Tasks 3 to 5 implement the neutral core and wrapper rewiring. Tasks 6 to 8 prove, publish, and synchronize the result.

---

### Task 1: Freeze the Linux Full-Authoritative Contract

**Files:**
- Create: `docs/universalization/linux-full-authoritative-contract.md`
- Modify: `docs/universalization/platform-support-matrix.md`
- Modify: `docs/universalization/platform-parity-contract.md`
- Modify: `docs/status/non-regression-proof-bundle.md`

**Objective:** Define exactly what Linux full-authoritative means before any implementation starts.

**Step 1: Write the contract**

Capture:

- required entry points
- required receipts
- required deep-check surfaces
- required no-regression conditions
- explicit blockers that keep Linux below `full-authoritative`

**Step 2: Freeze acceptance criteria**

State exact criteria for:

- `install.sh`
- `scripts/bootstrap/one-shot-setup.sh`
- `check.sh --profile full --deep`
- freshness gate
- coherence gate
- bootstrap doctor gate
- MCP materialization path

**Step 3: Record stop rules**

Document immediate stop conditions:

- Windows baseline regression
- receipt schema drift
- shell path false positives
- documentation overclaim

**Step 4: Run truth consistency review**

Run:

```powershell
git diff --check
pwsh -NoProfile -File .\scripts\verify\vibe-platform-support-contract-gate.ps1 -WriteArtifacts
```

**Expected:** no contradiction between contract docs and current support labels.

**Step 5: Commit**

```bash
git add docs/universalization/linux-full-authoritative-contract.md docs/universalization/platform-support-matrix.md docs/universalization/platform-parity-contract.md docs/status/non-regression-proof-bundle.md
git commit -m "docs: freeze linux full-authoritative contract"
```

---

### Task 2: Design the Runtime-Neutral Authoritative Core

**Files:**
- Create: `docs/design/runtime-neutral-authoritative-core.md`
- Modify: `install.sh`
- Modify: `check.sh`
- Modify: `scripts/bootstrap/one-shot-setup.sh`
- Create: `scripts/verify/runtime_neutral/README.md`

**Objective:** Design the shared authoritative execution model before changing any gate implementation.

**Step 1: Choose the neutral runtime**

Default choice is Python because:

- shell fallback logic already uses Python in bootstrap paths
- JSON/receipt handling is easier to preserve across platforms
- Linux and Windows both already depend on Python in practical setup flows

**Step 2: Define the neutral-core boundaries**

The core must own:

- freshness evaluation
- coherence evaluation
- bootstrap doctor evaluation
- stable JSON receipt emission

Wrappers must only:

- parse shell args
- locate repo roots
- call the neutral core
- map exit codes

**Step 3: Freeze wrapper responsibilities**

- `install.ps1` and `check.ps1` remain supported wrappers on Windows
- `install.sh` and `check.sh` become first-class wrappers, not degraded approximations
- no business logic remains shell-exclusive unless contractually justified

**Step 4: Define parity test strategy**

On Windows, every new neutral-core surface must be dual-run against the existing PowerShell behavior until parity is proved.

**Step 5: Commit**

```bash
git add docs/design/runtime-neutral-authoritative-core.md scripts/verify/runtime_neutral/README.md install.sh check.sh scripts/bootstrap/one-shot-setup.sh
git commit -m "plan: define runtime-neutral authoritative core design"
```

---

### Task 3: Extract Installed Runtime Freshness Into the Neutral Core

**Files:**
- Create: `scripts/verify/runtime_neutral/freshness_gate.py`
- Modify: `scripts/verify/vibe-installed-runtime-freshness-gate.ps1`
- Modify: `install.sh`
- Modify: `check.sh`
- Create: `tests/runtime_neutral/test_freshness_gate.py`

**Objective:** Remove the `pwsh` hard dependency from authoritative freshness checks while preserving receipt semantics.

**Step 1: Write the failing tests**

Cover:

- canonical repo root resolution
- installed runtime metadata loading
- receipt schema stability
- pass/fail parity with expected stale vs fresh inputs

**Step 2: Run the tests and verify they fail**

Run:

```bash
pytest tests/runtime_neutral/test_freshness_gate.py -v
```

**Expected:** fail because the neutral freshness core does not exist yet.

**Step 3: Implement the minimal neutral freshness core**

Requirements:

- accept target root
- emit the same decision categories
- write the same receipt fields or a versioned superset
- return non-zero on freshness failure

**Step 4: Keep PowerShell wrapper compatibility**

Update `vibe-installed-runtime-freshness-gate.ps1` so it can either:

- keep current behavior, or
- delegate to the neutral core while preserving CLI compatibility

**Step 5: Rewire shell surfaces**

- `install.sh` must stop warning-and-skipping solely because `pwsh` is absent
- `check.sh` must execute the freshness gate directly through the neutral core

**Step 6: Verify**

Run:

```bash
pytest tests/runtime_neutral/test_freshness_gate.py -v
bash ./check.sh --skip-runtime-freshness-gate
```

Run on Windows:

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-installed-runtime-freshness-gate.ps1 -TargetRoot "$PWD" -WriteReceipt
```

**Expected:** tests pass; Linux no longer depends on `pwsh` for freshness; Windows receipt remains valid.

**Step 7: Commit**

```bash
git add scripts/verify/runtime_neutral/freshness_gate.py scripts/verify/vibe-installed-runtime-freshness-gate.ps1 install.sh check.sh tests/runtime_neutral/test_freshness_gate.py
git commit -m "feat: extract runtime-neutral freshness gate"
```

---

### Task 4: Extract Runtime Coherence and Bootstrap Doctor Into the Neutral Core

**Files:**
- Create: `scripts/verify/runtime_neutral/coherence_gate.py`
- Create: `scripts/verify/runtime_neutral/bootstrap_doctor.py`
- Modify: `scripts/verify/vibe-release-install-runtime-coherence-gate.ps1`
- Modify: `scripts/verify/vibe-bootstrap-doctor-gate.ps1`
- Modify: `check.sh`
- Modify: `scripts/bootstrap/one-shot-setup.sh`
- Create: `tests/runtime_neutral/test_coherence_gate.py`
- Create: `tests/runtime_neutral/test_bootstrap_doctor.py`

**Objective:** Remove the remaining authoritative `pwsh` dependency from Linux deep-check closure.

**Step 1: Write the failing tests**

Cover:

- release/install/runtime mismatch detection
- bootstrap doctor failure classification
- profile materialization expectations
- warning vs fail boundary

**Step 2: Run tests to prove the gap**

Run:

```bash
pytest tests/runtime_neutral/test_coherence_gate.py tests/runtime_neutral/test_bootstrap_doctor.py -v
```

**Expected:** fail before implementation.

**Step 3: Implement the neutral coherence gate**

Keep parity for:

- release version comparison
- installed marker comparison
- target root vs installed root validation
- exit code mapping

**Step 4: Implement the neutral bootstrap doctor**

Doctor must cover the same authoritative surfaces currently guarded by:

- `vibe-bootstrap-doctor-gate.ps1`

including:

- installed files expected to exist
- profile materialization expectations
- readiness of critical runtime directories

**Step 5: Rewire Linux deep-check path**

- `check.sh --deep` must run doctor without `pwsh`
- `one-shot-setup.sh` must stop ending in “doctor skipped because pwsh is absent” when the neutral doctor is available

**Step 6: Preserve PowerShell wrapper compatibility**

Windows must still be able to run the original PowerShell entry points.

**Step 7: Verify**

Run:

```bash
pytest tests/runtime_neutral/test_coherence_gate.py tests/runtime_neutral/test_bootstrap_doctor.py -v
bash ./scripts/bootstrap/one-shot-setup.sh
bash ./check.sh --profile full --deep
```

Run on Windows:

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-release-install-runtime-coherence-gate.ps1 -TargetRoot "$PWD"
pwsh -NoProfile -File .\scripts\verify\vibe-bootstrap-doctor-gate.ps1 -TargetRoot "$PWD" -WriteArtifacts
```

**Expected:** Linux executes doctor and coherence authoritatively without `pwsh`; Windows wrappers still pass.

**Step 8: Commit**

```bash
git add scripts/verify/runtime_neutral/coherence_gate.py scripts/verify/runtime_neutral/bootstrap_doctor.py scripts/verify/vibe-release-install-runtime-coherence-gate.ps1 scripts/verify/vibe-bootstrap-doctor-gate.ps1 check.sh scripts/bootstrap/one-shot-setup.sh tests/runtime_neutral/test_coherence_gate.py tests/runtime_neutral/test_bootstrap_doctor.py
git commit -m "feat: extract runtime-neutral coherence and doctor gates"
```

---

### Task 5: Converge Wrapper Behavior Without Weakening Windows

**Files:**
- Modify: `install.sh`
- Modify: `check.sh`
- Modify: `install.ps1`
- Modify: `check.ps1`
- Modify: `scripts/bootstrap/one-shot-setup.sh`
- Modify: `scripts/bootstrap/one-shot-setup.ps1`
- Create: `tests/runtime_neutral/test_wrapper_parity.py`

**Objective:** Make shell and PowerShell wrappers consume the same authority semantics while preserving Windows release authority.

**Step 1: Write parity tests**

Cover:

- wrapper argument mapping
- exit code parity
- receipt location parity
- warning message classification

**Step 2: Implement minimal wrapper convergence**

Wrappers may differ in shell syntax, but not in:

- gate selection
- target-root semantics
- receipt meaning
- failure severity

**Step 3: Preserve Windows-first operator ergonomics**

Keep:

- PowerShell commands documented and usable
- Windows release authority explicitly intact

Do **not** demote PowerShell into an unsupported compatibility shim.

**Step 4: Verify**

Run:

```bash
pytest tests/runtime_neutral/test_wrapper_parity.py -v
```

Run Windows parity bundle:

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-platform-doctor-parity-gate.ps1 -WriteArtifacts
```

**Expected:** wrappers differ only in invocation surface, not in authoritative outcome semantics.

**Step 5: Commit**

```bash
git add install.sh check.sh install.ps1 check.ps1 scripts/bootstrap/one-shot-setup.sh scripts/bootstrap/one-shot-setup.ps1 tests/runtime_neutral/test_wrapper_parity.py
git commit -m "refactor: converge shell and powershell authoritative wrappers"
```

---

### Task 6: Build the Proof Bundle and Promotion Gates

**Files:**
- Create: `scripts/verify/vibe-runtime-neutral-gate-parity.ps1`
- Create: `scripts/verify/vibe-linux-full-authoritative-gate.ps1`
- Create: `scripts/verify/vibe-linux-doctor-closure-gate.ps1`
- Create: `docs/status/linux-full-authoritative-proof-bundle-2026-03-13.md`
- Modify: `docs/status/non-regression-proof-bundle.md`

**Objective:** Make Linux promotion depend on hard evidence rather than narrative.

**Step 1: Create parity gate**

Compare Windows PowerShell wrapper output against neutral-core output on the same machine.

**Step 2: Create Linux full-authoritative gate**

This gate should fail unless all Linux acceptance criteria are satisfied.

**Step 3: Create Linux doctor closure gate**

This gate should prove that:

- doctor actually ran
- doctor did not silently skip authoritative surfaces
- receipts and artifacts exist

**Step 4: Produce proof bundle template**

Bundle must include:

- commands
- environment prerequisites
- receipts
- gate outputs
- final support judgment

**Step 5: Verify**

Run:

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-runtime-neutral-gate-parity.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-linux-full-authoritative-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-linux-doctor-closure-gate.ps1 -WriteArtifacts
```

**Expected:** promotion can only pass when all evidence surfaces exist and agree.

**Step 6: Commit**

```bash
git add scripts/verify/vibe-runtime-neutral-gate-parity.ps1 scripts/verify/vibe-linux-full-authoritative-gate.ps1 scripts/verify/vibe-linux-doctor-closure-gate.ps1 docs/status/linux-full-authoritative-proof-bundle-2026-03-13.md docs/status/non-regression-proof-bundle.md
git commit -m "test: add linux full-authoritative proof gates"
```

---

### Task 7: Run the Fresh-Machine Matrix and Decide Promotion

**Files:**
- Create: `docs/status/platform-linux-full-authoritative-closure-report-2026-03-13.md`
- Modify: `adapters/codex/platform-linux.json`
- Modify: `docs/universalization/platform-support-matrix.md`
- Modify: `docs/universalization/platform-parity-contract.md`
- Modify: `scripts/verify/vibe-platform-doctor-parity-gate.ps1`

**Objective:** Upgrade support labels only if proof passes.

**Step 1: Run Windows control baseline**

Run:

```powershell
pwsh -NoProfile -File .\check.ps1 -Profile full -Deep
pwsh -NoProfile -File .\scripts\verify\vibe-platform-support-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-platform-doctor-parity-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-version-consistency-gate.ps1 -WriteArtifacts
```

**Step 2: Run Linux fresh-machine full-authoritative rehearsal**

Run:

```bash
bash ./scripts/bootstrap/one-shot-setup.sh
bash ./check.sh --profile full --deep
```

Then run proof gates from a PowerShell-capable control environment if required by current governance.

**Step 3: Compare results against acceptance contract**

If any blocker remains, Linux stays below `full-authoritative`.

**Step 4: Only if all gates pass, upgrade platform contract**

Promote:

- `adapters/codex/platform-linux.json`
- support docs
- parity gate expectations

**Step 5: Verify**

Run:

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-platform-support-contract-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-universalization-no-regression-gate.ps1 -WriteArtifacts
```

**Expected:** either:

- Linux is promoted with proof, or
- Linux remains constrained with an explicit blocker report

Both outcomes are acceptable. False promotion is not.

**Step 6: Commit**

```bash
git add docs/status/platform-linux-full-authoritative-closure-report-2026-03-13.md adapters/codex/platform-linux.json docs/universalization/platform-support-matrix.md docs/universalization/platform-parity-contract.md scripts/verify/vibe-platform-doctor-parity-gate.ps1
git commit -m "docs: close linux platform authority decision"
```

---

### Task 8: Publish the Result Without Overclaim and Synchronize Versions

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `docs/cold-start-install-paths.md`
- Modify: `docs/status/current-state.md`
- Modify: `docs/status/roadmap.md`
- Modify: `config/version-governance.json`

**Objective:** Make public install guidance match the proven truth, and synchronize repo/runtime/version governance.

**Step 1: Update the install story**

README must clearly distinguish:

- minimal usable path
- recommended full path
- enterprise-governed path

For Linux, “full path” can only mean full-authoritative if Task 7 proved it.

**Step 2: Sync versions**

Ensure:

- local repo version
- bundled/runtime version markers
- GitHub-visible version documentation

all point to the same current truth.

**Step 3: Run final no-regression bundle**

Run:

```powershell
pwsh -NoProfile -File .\scripts\verify\vibe-version-packaging-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-universalization-no-regression-gate.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\governance\phase-end-cleanup.ps1 -WriteArtifacts
pwsh -NoProfile -File .\scripts\verify\vibe-node-zombie-gate.ps1 -WriteArtifacts
```

**Expected:** clean version state, no unmanaged node residue, no public doc overclaim.

**Step 4: Commit**

```bash
git add README.md README.en.md docs/cold-start-install-paths.md docs/status/current-state.md docs/status/roadmap.md config/version-governance.json
git commit -m "docs: publish linux authority result and sync versions"
```

---

## Test Matrix

### Required environments

1. Windows authoritative control machine
2. Linux fresh machine with Python only
3. Linux fresh machine with Python and `pwsh`

### Required test categories

| Category | Windows | Linux + `pwsh` | Linux without `pwsh` | Pass condition |
| --- | --- | --- | --- | --- |
| freshness gate | required | required | required | no silent skip |
| coherence gate | required | required | required | same failure semantics |
| bootstrap doctor | required | required | required | authoritative doctor exists |
| one-shot setup | required | required | required | no misleading success |
| wrapper parity | required | compare | compare | same receipt meaning |
| proof bundle | required | required | required | promotion or honest non-promotion |

### Stability rule

Linux must pass the full-authoritative matrix on at least:

- 2 clean Linux environments
- 3 consecutive end-to-end rehearsals

before any promotion is merged.

## Stop Rules

Stop the migration immediately if:

- Windows authoritative baseline fails
- receipt schema drifts unexpectedly
- Linux “passes” by skipping a gate
- documentation says `full-authoritative` before proof exists
- neutral core and wrapper output disagree on Windows

## Rollback Plan

Rollback order is fixed:

1. remove public support-level upgrade
2. restore `platform-linux.json` to the previous status
3. disable promotion gates that assume Linux authority
4. keep neutral-core code only if it still passes Windows and constrained-Linux paths
5. if neutral-core change caused a Windows regression, revert the core extraction batch

## Completion Criteria

This migration is complete only if:

1. Windows remains fully green as the release-authority lane.
2. Linux runs freshness, coherence, and bootstrap doctor without mandatory `pwsh`.
3. Linux fresh-machine proof bundle passes on repeated runs.
4. Public docs match the real support level.
5. Version governance is synchronized after the decision.
6. No functional regression is introduced on install, check, doctor, or receipts.

If Linux still fails proof after all planned extraction work, the migration is **not** a failure as long as the repo exits with:

- stronger truth
- explicit blockers
- preserved Windows authority
- no false claim

That is the required zero-regression outcome.

## Execution Handoff

This document is retained as the frozen migration plan for the Linux full-authoritative track.
