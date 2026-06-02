# iOS Accessibility Audit Workflow (Code-Only)

## Table of Contents

- Scope
- Status Vocabulary
- Severity Guidelines
- Audit Sequence
- Reporting Format (Markdown)
- Manual Checks for User (Only If Needed)
- Static-Evidence Limits
- Evidence Quality Rules

## Scope

Use this workflow for native iOS feature audits (`SwiftUI`, `UIKit`) based on source code inspection.

Do not run the app, simulator, or UI tests as part of this skill. If behavior is not derivable from code, mark it as a user follow-up check instead of guessing.

Standards model:

- WCAG 2.2 Level A/AA = primary standard
- WCAG2Mobile = interpretation guidance for applying WCAG to mobile apps

## Status Vocabulary

Use exactly one status per success criterion in your internal SC tracking (a matrix/table is optional and usually should not be output unless the user asks):

- `Pass`
- `Fail`
- `Partial`
- `Needs user verification` (code suggests intent, but behavior is not provable statically)
- `Not applicable`
- `Not assessable` (required source/evidence missing from repo or scope)

Use `Needs user verification` instead of asserting `Pass` for visual measurements, screen-reader output, or live focus behavior.

## Severity Guidelines

Use a pragmatic engineering severity model:

- `Critical`: Blocks task completion or access in a core flow for a user group.
- `High`: Likely causes major friction or failure in a common flow.
- `Medium`: Material issue with workaround or narrower scope.
- `Low`: Lower-impact issue, edge case, or quality gap.

## Audit Sequence

1. Define the scoped feature flow.
2. List in-scope screens/states:
   - initial screen
   - modal/sheet/dialog states
   - loading/empty/error/success states
3. Find the actual UI implementations:
   - SwiftUI `View` types
   - `UIViewController` classes
   - custom `UIView` controls
4. Inventory interactive elements and semantic surfaces:
   - buttons
   - fields
   - toggles
   - custom controls
   - images/icons that convey meaning
5. Run the SC checklist in `ios-audit-checklist.md`.
6. Use `ios-accessibility-api-examples.md` to validate interpretation of APIs and patterns.
7. Produce a Markdown report:
   - severity-ordered findings
   - internal SC status tracking (table optional, usually hidden)
   - user follow-up checks (only when needed)
   - limitations/assumptions

## Reporting Format (Markdown)

Default reporting guidance for this workflow:

- Be concise and findings-first.
- Keep SC status tracking internal unless the user explicitly asks for a table/matrix.
- For the merged SwiftUI+WCAG skill, follow the strict finding template in that skill's `SKILL.md`.

If no skill-specific template overrides this workflow, include:

- findings with evidence and WCAG mapping
- user follow-up checks (only when needed)
- assumptions/limitations (when material)

## Manual Checks for User (Only If Needed)

Create a manual-check list when code cannot prove behavior. Typical cases:

- contrast ratios
- actual rendered tap target size/spacing
- VoiceOver reading order and announcements
- focus visibility / focus clipping
- orientation/reflow behavior on device
- live status message timing

Keep checks short, reproducible, and tied to a screen and user action.

## Static-Evidence Limits

Do not assert `Pass` solely from code for:

- color contrast ratios
- rendered target size measurements
- final reading order announced by VoiceOver
- visual focus indicators
- clipping/overlap at large text sizes
- animation flashing thresholds

Use `Needs user verification` and add a concrete manual check.

## Evidence Quality Rules

Prefer evidence from the code that renders the feature, not only shared wrappers.

For each finding, cite:

- file path
- type/function/symbol name when available
- relevant modifier/property or missing semantic hook
- why the observed code pattern maps to the WCAG issue
