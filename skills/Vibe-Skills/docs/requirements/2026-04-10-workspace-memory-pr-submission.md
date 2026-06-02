# Workspace Memory PR Submission

## Goal

Package the workspace-shared memory enhancement into an isolated, reviewable PR that explains the behavior clearly to both maintainers and end users.

## Scope

- include the workspace memory plane runtime/config/schema/docs/tests needed for same-workspace shared memory and progressive disclosure
- include the quantitative Codex simulation proof and workspace isolation proof
- update the root English and Chinese README memory sections with a plain-language explanation
- keep the PR isolated from unrelated local changes already present in the original working tree

## Constraints

- preserve high cohesion and low coupling
- do not re-enable any legacy memory downgrade path
- describe hard-fail behavior clearly when the workspace broker is unavailable
- do not claim success without fresh verification evidence from the isolated PR branch

## Acceptance

- PR branch diff is limited to memory-plane/runtime/docs/test surfaces relevant to this enhancement
- README explains same-workspace sharing, cross-workspace isolation, relevance-gated recall, and progressive disclosure in plain language
- targeted memory regression suite passes on the isolated branch
- a reviewer can understand the change set and verification story without reading the full chat history
