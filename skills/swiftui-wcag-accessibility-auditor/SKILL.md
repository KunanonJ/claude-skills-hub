---
name: swiftui-wcag-accessibility-auditor
description: Audit SwiftUI iOS feature code for accessibility against WCAG 2.2 Level A/AA and return patch-ready fixes. Use when reviewing SwiftUI views/screens (including auth, forms, settings, and custom controls) and you need both standards traceability (WCAG + WCAG2Mobile interpretation) and practical, minimal code changes in a concise priority-grouped Markdown format with user follow-up checks for code-indeterminate behavior.
---

# SwiftUI WCAG Accessibility Auditor

## Overview

Audit SwiftUI iOS features with a dual mode:

- WCAG-driven coverage and evidence (`what fails / what is uncertain / why`)
- SwiftUI patch-ready remediation (`what to change with minimal code edits`)

Treat this as a code audit. Do not run the app. If a result cannot be proven from source, mark it as `Needs user verification` and add a concrete user follow-up check.

## When to Use This Skill vs Nearby Skills

Use this merged skill when you need both:

- WCAG 2.2 mapping / traceability, and
- SwiftUI-specific fixes/snippets

Prefer the other skills when:

- `mobile-accessibility-audit`: feature may include `UIKit` or you only need standards-first audit coverage
- `swiftui-accessibility-auditor`: you want a fast SwiftUI-only heuristic review without WCAG traceability

## Load Order

1. Read `references/ios-audit-workflow.md` for code-only audit process, statuses, evidence rules, and baseline report format.
2. Read `references/ios-audit-checklist.md` for WCAG SC coverage priorities and code signals.
3. Read `references/wcag2mobile-ios-reference.md` when interpreting mobile-specific applicability or draft maturity of a criterion.
4. Read `references/ios-accessibility-api-examples.md`, starting with the SwiftUI sections only.
5. Read `references/swiftui-remediation-guide.md` for patch strategy, non-goals, priority model, and SwiftUI fix patterns.
6. Use `references/swiftui-manual-checklist.md` only when generating user follow-up checks or a final manual validation list.

## Scope Rules

- Audit native iOS SwiftUI code only.
- Audit `UIViewRepresentable` / `UIViewControllerRepresentable` bridges only to the extent they affect the SwiftUI feature.
- If the feature delegates core behavior to UIKit, say so and either narrow the audit or recommend using `mobile-accessibility-audit`.
- Do not broaden scope to macOS, watchOS, web, or non-SwiftUI implementations.

## Audit Execution (Merged Workflow)

1. Define the scoped feature flow and in-scope screens/states.
2. Identify the SwiftUI entry views and related subviews for the feature.
3. Run the WCAG checklist (`ios-audit-checklist.md`) and record evidence with statuses.
4. Use the SwiftUI API examples to avoid false positives and identify missing semantics.
5. Generate patch-ready fix suggestions using `swiftui-remediation-guide.md`.
6. Produce a Markdown report with:
   - prioritized findings (`P0`, `P1`, `P2`)
   - WCAG SC mapping for each finding
   - patch-ready snippet embedded in each finding
   - user follow-up checks (only for code-indeterminate items)

## Output Format (Strict, Concise)

Be concise. Use the following structure exactly.

Rules:

- Group findings by priority using top-level headings: `# Findings - P0`, `# Findings - P1`, `# Findings - P2`
- Omit empty priority groups.
- Put the code snippet in the same finding section (not in a separate snippets section).
- Omit the WCAG coverage matrix unless the user explicitly asks for it.
- Add `# Scope / Assumptions` only if ambiguity materially affects the audit.
- Add `# User Follow-Up Checks` only if there are `Needs user verification` items.

Template for each finding:

````md
# Findings - P1

## 1. <Problem name>
- **What**: <problem description with code evidence>
- **Where**: <file path + line(s)>
- **Fix suggestion**: <suggested fix in words>
- **WCAG**: <SC # - Title (Level)>

```swift
// patch-ready snippet
```
````

Notes:

- Include `Confidence` inside `*What*` when useful (for example: `Likely issue (confidence: medium)`).
- Keep snippets minimal and directly applicable to the cited code path.
- If no code snippet is appropriate, state why in `*Fix suggestion*` (rare).

## Practical Search Guidance (SwiftUI-first)

Start in the feature path and prefer SwiftUI symbols first:

```bash
rg --files | rg '\\.(swift)$'
rg -n "struct .*View: View|body: some View|NavigationStack|sheet\\(|fullScreenCover\\(" .
rg -n "accessibility(Label|Hint|Value|Hidden)|accessibility(AddTraits|RemoveTraits)|accessibilityElement\\(|accessibilityFocused\\(" .
rg -n "@AccessibilityFocusState|onTapGesture|DragGesture|lineLimit\\(|minimumScaleFactor|dynamicTypeSize" .
```

Then consult `references/ios-accessibility-api-examples.md` for pattern interpretation.

## Example Requests

- `Use $swiftui-wcag-accessibility-auditor to audit this SwiftUI checkout feature against WCAG 2.2 and return prioritized findings with patch-ready fixes in the strict finding format.`
- `Use $swiftui-wcag-accessibility-auditor to review this SwiftUI login + OTP flow for accessible authentication (3.3.8) and suggest minimal code changes.`
- `Use $swiftui-wcag-accessibility-auditor to audit this settings screen and produce user follow-up checks only for contrast, target size, and VoiceOver announcement timing.`

## Resources

- `references/ios-audit-workflow.md`: code-only audit process, statuses, evidence quality rules, and report structure.
- `references/ios-audit-checklist.md`: iOS WCAG checklist and SC coverage priorities.
- `references/wcag2mobile-ios-reference.md`: cleaned mobile interpretation reference (WCAG2Mobile/WCAG2ICT distilled for iOS audits).
- `references/ios-accessibility-api-examples.md`: SwiftUI + UIKit API examples (use SwiftUI sections first in this skill).
- `references/swiftui-remediation-guide.md`: SwiftUI patch strategy, non-goals, priorities, and fix patterns.
- `references/swiftui-manual-checklist.md`: compact user manual validation checklist for follow-up checks.
