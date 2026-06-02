# Public Skill Surface Decoupling Requirement

## Goal

Refactor install, uninstall, and runtime packaging so Vibe-Skills exposes a minimal public skill surface by default while preserving the governed `vibe` runtime, host integrations, routing behavior, and verification guarantees.

## Problem Statement

The current `full` install profile projects nearly the entire bundled skill corpus into `<TARGET_ROOT>/skills/*`.
That creates three structural problems:

1. host-visible surface area is much larger than the canonical user entry
2. install and uninstall ownership spread across multiple projections and generated compatibility roots
3. users perceive Vibe-Skills as "installing 300+ visible skills" instead of "installing one governed runtime with internal capability packs"

The repository already contains partial support for a narrower surface:

- canonical runtime is projected to `skills/vibe`
- `minimal` profile already uses allowlisted top-level skills
- skill catalog metadata and capability catalog governance already distinguish runtime authority from discovery corpus

The missing piece is a single coherent payload model that makes the public skill surface intentionally small instead of accidentally broad.

## Desired Outcome

The default install experience should make `vibe` the only required public skill entry, or at most a very small public runtime set that exists only for proven host compatibility.
Most bundled specialist skills should become internal managed payload under the canonical Vibe-owned tree and should not need to appear as peer top-level skill directories.

## Architecture Intent

The refactor should establish one explicit rule:

- capability breadth is not the same thing as public host-visible surface breadth

After the refactor, the system should distinguish three different concerns instead of projecting them through the same top-level `skills/` directory:

1. public skill surface
2. internal specialist corpus
3. compatibility projections

The public surface is what host tooling is expected to discover directly.
The internal corpus is what Vibe itself consumes to resolve specialist descriptions and recommendations.
Compatibility projections are opt-in or host-scoped derived outputs used only when a host or migration path still requires them.

## Scope

In scope:

- runtime-core packaging profile semantics
- installer-core materialization and uninstall ownership
- skill catalog consumption and managed inventory boundaries
- host-visible skill surface policy
- generated compatibility topology rules
- docs and verification updates needed to preserve truthful claims

Out of scope:

- changing the governed runtime contract of `vibe`
- removing bounded compatibility shims with active callers unless replacement proof exists
- redesigning custom user-owned skill governance
- changing host bridge commands or provider connectivity behavior

## Functional Requirements

1. Default install profile must expose `skills/vibe` as the canonical public runtime root.
2. Broad specialist skill payload must be installable without requiring peer top-level `skills/<official-skill>/` directories by default.
3. Routing and capability recommendation behavior must continue to work when specialist content is internalized.
4. Hosts that need explicit visible surfaces must declare those surfaces explicitly through a small compatibility projection rather than inheriting the whole bundled corpus.
5. Uninstall must be able to remove all Vibe-owned payload from a target root without relying on broad filesystem scans to infer ownership.
6. Generated compatibility roots must remain derived outputs and must not become parallel ownership sources.
7. `minimal` and `full` profiles must remain semantically distinct, but the distinction should be based on internal capability breadth and optional compatibility projections rather than "few visible skills vs hundreds of visible skills."
8. Runtime descriptor loading must stop treating top-level installed official skill directories as the primary installed-runtime truth surface.
9. Installer ownership records must become authoritative enough for uninstall to remove Vibe-owned trees and roll back managed JSON/config mutations deterministically.
10. The rollout must support a temporary legacy compatibility mode so host regressions can be mitigated without reverting the internal corpus refactor.

## Acceptance Criteria

1. Installing the default broad profile no longer creates hundreds of peer top-level official skill directories under `<TARGET_ROOT>/skills/`.
2. `vibe` remains discoverable and functional for all supported hosts that currently rely on it.
3. Host-specific wrappers, managed JSON/config writes, and specialist bridge wrappers continue to work.
4. Reinstall, upgrade, profile change, and uninstall flows remain deterministic and owned-only.
5. Existing runtime freshness and coherence gates remain truthful after the topology change.
6. Capability/routing behavior that depends on the catalog continues to resolve internal specialist recommendations without requiring those skills to be top-level host-visible.
7. `vibe`-driven routing and governed execution must remain operational on `codex`, `claude-code`, `openclaw`, and `opencode`.
8. Governance-layer behavior must continue to honor the six-stage runtime contract, root/child lane rules, and cleanup receipts.
9. Memory-layer behavior must continue to match README-level claims for session/project/short-term/long-term roles, explicit-write rules, and context-fold behavior.
10. README-level product claims about routing, governance, memory, install management, and uninstall behavior must remain provable by tests or runtime probes.

## Product Acceptance Checks

- A fresh default install on Codex leaves a clean `skills/` root centered on `vibe`.
- OpenCode preview still detects `vibe` and its installed agents.
- Downgrade/upgrade flows do not strand previously managed public skills.
- Uninstall preview and actual uninstall report only Vibe-owned content and leave no managed residue.
- Full profile still offers broader capability coverage than minimal even if both now present a narrow public `skills/` surface.
- If legacy compatibility projection is enabled for a host, that projection is explicit, test-backed, and removable without changing runtime authority.
- `codex`, `claude-code`, `openclaw`, and `opencode` each pass at least one realistic end-to-end `vibe` task scenario plus install/check/uninstall probe coverage.
- Routing probes demonstrate that `vibe` can still invoke or route toward specialist help under representative planning, debug, and governed-execution tasks.
- Governance probes demonstrate stage order, root/child constraints, and cleanup outputs.
- Memory probes demonstrate activation/folding behavior and no silent drift from the four-tier memory description in the README.

## Manual Spot Checks

- Inspect `<TARGET_ROOT>/skills/` after install for top-level skill count.
- Inspect `<TARGET_ROOT>/skills/vibe/` for internal catalog and capability payload placement.
- Run host check flows from the installed runtime.
- Verify reinstall from prior broad installs prunes obsolete public projections.
- Verify uninstall removes generated nested compatibility content and sidecars.

## Constraints

- Keep canonical semantic ownership in package-owned cores.
- Do not let catalog or discovery corpus become a second runtime authority.
- Do not break hosts that currently rely on `skills/vibe` visibility or agent/config surfaces.
- Prefer additive compatibility migration over flag-day deletion.
- Preserve detached `skill-catalog` metadata ownership; do not move routing truth into the catalog package.
- Treat `.vibeskills` and managed JSON/config mutations as sidecar ownership, not accidental install residue.

## Implementation Standards

### Subjective Goals

- High cohesion: each module should own one kind of truth only.
- Low coupling: public skill visibility, runtime descriptor resolution, install topology, and uninstall ownership should no longer depend on each other implicitly.
- Honest product surface: the default product should look like "one governed runtime with internal capability packs", not "hundreds of peer skills".
- Compatibility-first migration: behavior-preserving compatibility layers are preferred over abrupt deletion.
- Explicitness over filesystem guesswork: if runtime or uninstall depends on a path, that dependency should be represented in a contract or ledger instead of being inferred ad hoc.
- Small public surface, rich internal capability: broad capability coverage should live internally unless a host has a proven need for explicit public projection.

### Objective Standards

- No supported host may lose discoverability of `vibe`.
- `codex`, `claude-code`, `openclaw`, and `opencode` must each retain a working `$vibe` or equivalent governed entry path after the refactor.
- Default full install must stop creating hundreds of peer top-level official skill directories under `<TARGET_ROOT>/skills/`.
- Runtime descriptor resolution must succeed when official specialist skills exist only under the Vibe-owned internal corpus.
- Uninstall must remove all Vibe-owned runtime, compatibility, and sidecar payload without leaving managed residue.
- Managed JSON/config rollback must be deterministic, BOM-safe, and covered by tests.
- Any retained legacy public projection must be controlled by an explicit compatibility contract or toggle.
- Full and minimal profiles must remain observably distinct in capability breadth after the topology refactor.
- Docs, tests, and runtime contracts must describe the same steady-state topology.
- README-level claims for routing, governed execution, memory continuity, and host installation behavior must each map to concrete tests or probes.
- The implementation plan must include multi-task probe scenarios that exercise routing, runtime execution, governance, cleanup, and memory continuity on the supported host matrix.
- The validation plan must explicitly cover `codex`, `claude-code`, `openclaw`, and `opencode`.
- The validation plan must cover at least routing, governed runtime orchestration, uninstall safety, and memory/runtime activation.
- Validation must include realistic multi-task probes rather than only static contract assertions.
- Deep validation must cover `codex`, `claude-code`, `openclaw`, and `opencode` rather than relying on a single-host proof.
- Deep validation must cover routing, governed runtime, memory behavior, install/check/uninstall behavior, and README-truth probes as separate evidence classes.

## Non-Goals

- "Hide everything" by making routing depend on undocumented implicit paths
- move user-owned custom skills into Vibe-owned directories
- collapse verification, runtime, installer, and catalog responsibilities into a single module

## Delivery Truth Contract

Completion may be claimed only when the repo has:

- a documented target topology
- package and installer ownership changes aligned to that topology
- tests proving routing, install, reinstall, and uninstall still work under the new public surface model
- docs updated so they no longer imply that broad top-level skill projection is the intended default product surface
- an explicit compatibility-toggle and rollback story for hosts that still need legacy public projections during migration
