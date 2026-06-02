# Workspace Memory Phase Cleanup Audit Requirement

Date: 2026-04-10
Run ID: 20260410-workspace-memory-phase-cleanup-audit
Mode: interactive_governed
Runtime lane: root_governed

## Goal

Audit the current `workspace-memory-plane` implementation run in the local `Vibe-Skills` workspace and prepare a cautious end-of-phase cleanup checklist.

## Deliverable

A cleanup audit that:

- identifies likely task-created temporary files and directories
- distinguishes untracked implementation deliverables from removable residue
- provides explicit safe and unsafe cleanup guidance
- provides audit-first commands for `node` and `pwsh` process review and bounded targeting guidance for later manual use
- does not delete files or kill processes during the audit

## Constraints

- Work against the active repository root (`<repo-root>`)
- Base recommendations on the current repo state instead of generic cleanup advice
- Do not delete files, remove directories, or terminate processes
- Do not disturb unrelated workspaces, worktrees, or long-lived host tooling
- Keep guidance compatible with the governed phase-cleanup contract

## Acceptance Criteria

- The audit cites concrete current-repo paths or process evidence
- Safe-to-remove items are limited to clearly disposable scratch or ignored residue
- Unsafe items are called out when they may contain deliverables, evidence, or unrelated user work
- Process guidance prefers inspection and narrow PID targeting over broad `pkill` patterns

## Product Acceptance Criteria

- A maintainer can use the checklist at the end of a phase without risking active work
- The checklist separates workspace-memory deliverables from disposable runtime/test residue
- The process section is precise enough to avoid disturbing other repos or sessions

## Manual Spot Checks

- Inspect dirty tracked and untracked state with `git status --short --ignored`
- Inspect ignored scratch roots defined by `.gitignore`
- Inspect `.vibeskills` workspace-sidecar contents
- Inspect active `node` and `pwsh` processes with cwd and parentage context
- Inspect registered git worktrees before recommending any cleanup of `.worktrees/`

## Completion Language Policy

- Do not say an item is safe unless the current repo state supports that claim
- Use "conditionally safe" when an item is likely disposable but could still be user-owned
- Label all process cleanup commands as audit-first unless they only print information

## Delivery Truth Contract

- Audit-only engagement
- No cleanup actions executed
- Evidence before assertions

## Non-Goals

- Deleting residue during this run
- Reverting user changes
- Pruning worktrees or `/tmp` sandboxes without manual review
- General machine-wide process cleanup outside the relevant workspace

## Autonomy Mode

interactive_governed with inferred assumptions

## Inferred Assumptions

- The current dirty workspace represents an in-progress memory-plane implementation lane
- The user wants a cleanup checklist they can run manually at phase boundaries
- Ignored runtime proof under `outputs/` may need to survive until verification or archival is complete
