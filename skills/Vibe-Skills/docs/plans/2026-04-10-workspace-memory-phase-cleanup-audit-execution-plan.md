# Workspace Memory Phase Cleanup Audit Execution Plan

Date: 2026-04-10
Run ID: 20260410-workspace-memory-phase-cleanup-audit
Internal grade: L
Runtime lane: root_governed

## Scope

Audit the current workspace for cleanup boundaries by combining:

1. dirty-worktree inspection
2. ignored scratch and sidecar inspection
3. worktree and `/tmp` residue inspection
4. current `node` / `pwsh` process lineage inspection
5. final safe/unsafe checklist generation

## Serial Execution Units

1. Confirm repo root, branch, and current dirty state
2. Inspect `.gitignore` cleanup boundaries and ignored directories
3. Inspect untracked files to separate deliverables from residue
4. Inspect `.vibeskills`, `.tmp`, `outputs/`, and `.worktrees/`
5. Inspect live `node` / `pwsh` processes with cwd and parent-child context
6. Produce the audit checklist with explicit safe, conditional, and unsafe classes
7. Emit runtime receipts without deleting anything

## Ownership Boundaries

- Root lane owns the requirement, plan, receipts, and final cleanup checklist
- No child-governed execution lanes are required for this audit
- No cleanup command is executed beyond read-only inspection

## Verification Commands

- `export REPO_ROOT="<repo-root>"`
- `git -C "$REPO_ROOT" status --short --ignored`
- `git -C "$REPO_ROOT" worktree list --porcelain`
- `find "$REPO_ROOT/.tmp" -maxdepth 5 -type f -printf '%TY-%Tm-%Td %TH:%TM %s %p\n'`
- `find "$REPO_ROOT/outputs" -maxdepth 4 -printf '%TY-%Tm-%Td %TH:%TM %y %p\n'`
- `ps -eo pid,ppid,etimes,stat,comm,args --sort=etimes | rg 'node|pwsh|powershell'`
- `readlink /proc/<pid>/cwd`
- `rg -n '\\.vibeskills|\\.codex' "$REPO_ROOT"`

## Delivery Acceptance Plan

- Every cleanup recommendation must map to a concrete observed path or process pattern
- The final checklist must distinguish implementation artifacts from local residue
- Process termination advice must use narrow PID or cwd scoping

## Completion Language Rules

- Use "safe" only for clearly disposable ignored or scratch content
- Use "conditionally safe" for probable residue that still needs one manual confirmation step
- Use "unsafe" for tracked changes, untracked deliverables, workspace-sidecar data, or ambiguous active assets

## Rollback Rules

- Documentation-only repo additions
- Ignored runtime receipts only
- No source rollback or cleanup rollback needed because no destructive action is taken

## Phase Cleanup Expectations

- Preserve proof artifacts needed for later verification
- Treat `.tmp/`, `__pycache__/`, `.pytest_cache/`, and stale `/tmp/tmp*` sandboxes as cleanup candidates only after confirming inactivity
- Treat `.vibeskills/project.json` and `.vibeskills/memory/workspace-memory-plane.jsonl` as workspace-owned implementation artifacts
- Audit `.worktrees/` with `git worktree list --porcelain` before removing any worktree directory
