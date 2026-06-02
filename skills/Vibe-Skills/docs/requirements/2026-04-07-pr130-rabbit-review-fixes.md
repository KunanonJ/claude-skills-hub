# PR130 Rabbit Review Fixes

## Goal

Close the substantive review gaps on PR #130 so the branch can be re-published with prompt behavior and post-install guidance aligned to the real-host-root contract.

## Deliverable

- the English framework-only install prompt states the Codex real-host-root path as a host-specific rule instead of nesting it under the OpenCode branch
- the configuration guides restore concrete follow-up guidance for Windsurf, OpenClaw, and OpenCode after install
- regression tests cover both behaviors
- the existing PR branch is updated and pushed

## Constraints

- keep the fix scoped to the confirmed review findings
- preserve the already-landed real host root defaults across the six public hosts
- do not introduce a second source of truth that conflicts with the host-specific install guides
- do not revert unrelated changes already on the branch

## Acceptance Criteria

- `docs/install/prompts/framework-only-install.en.md` makes Codex guidance independently discoverable for prompt-following installers
- `docs/install/configuration-guide.en.md` and `docs/install/configuration-guide.md` tell users which real file or sidecar surface to inspect or edit for Windsurf, OpenClaw, and OpenCode
- targeted integration tests fail before the fix and pass after it
- the branch is committed, pushed, and the existing PR reflects the repair

## Product Acceptance Criteria

- a user following the English framework-only prompt for `codex` should be led to the real `~/.codex` path when immediate `$vibe` discoverability is required
- a user reading the configuration guide should be able to tell the difference between `installed locally` and `AI governance online-ready`, then find the concrete host-managed file or repo-owned sidecar they need next

## Manual Spot Checks

- inspect the final wording around the Codex and OpenCode branches in the English framework-only prompt
- inspect the final Windsurf, OpenClaw, and OpenCode sections in both configuration guides
- verify the diff stays limited to docs, tests, and governed planning artifacts

## Completion Language Policy

- do not claim the PR is updated until verification passes and the branch is pushed
- distinguish local fixes from remote PR publication

## Delivery Truth Contract

- report the exact verification commands run
- report the commit SHA and PR number after push

## Non-Goals

- redesign the broader install guidance set
- address style-only review nits that do not affect behavior or user completion
- change installer/runtime behavior outside the documented prompt and guidance fixes

## Autonomy Mode

- governed XL execution with bounded parallel analysis and local implementation

## Inferred Assumptions

- “收口” means fixing the confirmed blockers on the current PR rather than opening a new branch or new PR.
