# Vibe Host Bootstrap Deep Validation Requirement

## Summary

Perform a deep, temp-root-only validation of the new host global bootstrap injection path for `codex`, `claude-code`, and `opencode` so we can truthfully answer whether it is safe to use, whether it actually injects the managed bootstrap block, and whether the injected block materially pulls explicit `$vibe` or `/vibe` into canonical `vibe`.

## Goal

Prove the current implementation is non-destructive and operationally useful within the validated boundary, without touching real user home directories or host-native live environments.

## Deliverable

A governed validation result consisting of:

- one frozen execution plan for this validation run
- focused automated tests covering install, check, reinvoke, and uninstall safety
- temp-root manual spot-check evidence for all three supported hosts
- a truthful final report that distinguishes:
  - what is proven
  - what is strongly indicated but not host-kernel-proven
  - what remains out of scope

## Constraints

- do not install into or mutate the real user host roots
- do not write to:
  - `~/.codex`
  - `~/.claude`
  - `~/.config/opencode`
- all install, check, and uninstall validation must use isolated temporary target roots
- keep `vibe` as the only canonical governed runtime authority
- do not claim host-kernel hard enforcement if only bootstrap-level evidence exists
- if a useful guarantee cannot be proven in this environment, say so explicitly

## Acceptance Criteria

- automated validation covers `codex`, `claude-code`, and `opencode`
- for each supported host, install into a temp target root proves:
  - the correct global instruction file path is materialized
  - exactly one managed bootstrap block is inserted
  - the bootstrap receipt exists under `.vibeskills/global-instruction-bootstrap.json`
  - the bootstrap block contains explicit `$vibe` and `/vibe` entry wording
  - the bootstrap block states or implies canonical `vibe` authority rather than second-runtime authority
- install into an existing host instruction file preserves pre-existing user-authored content outside the managed block
- repeated install is idempotent and does not append a second managed block
- uninstall removes only the managed bootstrap block and preserves user-authored content
- if the file becomes installer-only and empty after removal, cleanup behavior is verified and reported truthfully
- check surfaces and bootstrap doctor stay green for healthy installs
- duplicate or corrupted managed blocks are detected as non-green states by automated tests or focused spot checks

## Product Acceptance Criteria

- within validated temp-root boundaries, a user can run install repeatedly without bootstrap duplication
- within validated temp-root boundaries, a user can uninstall without losing unrelated content in `AGENTS.md` or `CLAUDE.md`
- the injected text is short, explicit, and clearly routes explicit `$vibe` and `/vibe` toward canonical `vibe`
- final reporting does not overstate what this proves about real host runtime behavior

## Manual Spot Checks

- Codex temp root:
  - preseed `AGENTS.md` with user text
  - run install
  - inspect managed block markers and preserved user text
  - run check
  - rerun install
  - uninstall and verify block removal only
- Claude Code temp root:
  - preseed `CLAUDE.md` and `settings.json`
  - run install
  - inspect managed block, preserved text, managed `settings.json` node, and bootstrap receipt
  - run check
  - rerun install
  - uninstall and verify preserved user text
- OpenCode temp root:
  - preseed `AGENTS.md` and `opencode.json`
  - run install
  - inspect managed block and preserved text
  - run check
  - rerun install
  - uninstall and verify preserved user text while real config remains untouched

## Completion Language Policy

Do not claim the feature is fully safe or fully effective unless the final report separates:

- proven temp-root installer behavior
- repository-level routing pull evidence
- unproven live-host execution behavior

## Delivery Truth Contract

This validation succeeds only if the final report can point to fresh evidence showing all of the following:

- managed bootstrap injection happens for the three supported hosts
- injection is idempotent
- injection preserves unrelated user content
- uninstall removes only the managed block
- the injected text explicitly points `$vibe` and `/vibe` back to canonical `vibe`
- the system does not overclaim live-host enforcement beyond what temp-root and repo-level evidence can support

## Non-Goals

- do not prove undocumented host internals
- do not claim the host UI or host kernel definitely executes the injected guidance unless directly verified
- do not extend validation to unsupported hosts in this run
- do not redesign bootstrap wording unless testing exposes a real gap

## Autonomy Mode

Interactive governed execution with implementation allowed for missing or weak validation coverage.

## Assumptions

- temp-root installs exercise the same installer logic used for real installs
- the documented host instruction surfaces remain the intended consumption points
- usefulness can be partially proven by:
  - correct target file placement
  - explicit routing wording in the injected block
  - healthy `check` and bootstrap-doctor evidence
  - existing discoverability/runtime-neutral tests
