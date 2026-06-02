# WCAG2Mobile (iOS Audit) Distilled Reference

## Table of Contents

- Scope and Purpose
- Source Basis and Draft Maturity
- Normative vs Informative (How to Report Findings)
- Core Mobile Interpretation Rules Used by This Skill
- iOS Code-Audit Consequences of WCAG2Mobile/WCAG2ICT Framing
- Priority SC Reference (Mobile-Heavy)
- Core iOS UI SC Reference
- Practical Use in This Skill
- Source Provenance

## Scope and Purpose

This file is a cleaned, audit-focused distillation of the provided WCAG2Mobile draft source (`wcag_doc.md`) for native iOS code audits (`SwiftUI`, `UIKit`).

It keeps the parts that matter for an iOS code reviewer:

- what WCAG2Mobile says about applying WCAG 2.2 to mobile apps,
- how web terms map to mobile screens/views,
- where WCAG2Mobile adds mobile interpretation vs where it mostly defers to WCAG2ICT/WCAG intent,
- and how to apply that framing to an iOS code-only audit.

It intentionally omits:

- publication boilerplate,
- editor lists/history,
- links/issues except where draft maturity matters,
- repeated full WCAG/WCAG2ICT quoted text.

## Source Basis and Draft Maturity

Source basis:

- `/Users/romanmirzoyan/Developer/a11y-skill/wcag_doc.md`

Important maturity note (critical for audit quality):

- The WCAG2Mobile draft includes real mobile-specific text for some SCs, but many SC sections are still marked `Placeholder / Work In Progress`.
- For those placeholder sections, the practical guidance in this skill relies on:
  - WCAG 2.2 SC intent (normative baseline), plus
  - WCAG2ICT substitution/interpretation text, plus
  - iOS platform accessibility API evidence.

This means the agent should not overstate "WCAG2Mobile says X" when the source section is still a placeholder.

## Normative vs Informative (How to Report Findings)

Use this model in reports:

- **Normative standard:** WCAG 2.2 Level A/AA success criteria
- **Informative interpretation:** WCAG2Mobile (and WCAG2ICT where WCAG2Mobile defers or is incomplete)

Report findings as:

- `Likely failure of WCAG 2.2 SC X.Y.Z`, with
- a mobile/iOS interpretation note informed by WCAG2Mobile/WCAG2ICT.

Do not report findings as "failing WCAG2Mobile" (WCAG2Mobile is informative guidance, not a conformance standard).

## Core Mobile Interpretation Rules Used by This Skill

Derived from the WCAG2Mobile draft's background/guidance sections.

### 1. Web-to-mobile terminology mapping

Use these substitutions when interpreting WCAG language in mobile app audits:

- `web page` -> `screen` / `view`
- `set of web pages` -> `set of screens`

### 2. Unit of evaluation in this skill

Treat the primary unit of evaluation as:

- a single iOS screen/view in the scoped feature flow

When a criterion depends on consistency across multiple screens, evaluate:

- the `set of screens` in that feature flow (not the entire app by default)

### 3. Scope boundaries inherited from WCAG2Mobile framing

WCAG2Mobile (draft) frames guidance as:

- informative only,
- focused on Level A/AA,
- focused on mobile applications,
- not sufficient by itself for all product accessibility requirements.

Practical effect for this skill:

- audit WCAG 2.2 A/AA coverage in iOS code,
- note limitations,
- do not claim certification/conformance from code review alone.

## iOS Code-Audit Consequences of WCAG2Mobile/WCAG2ICT Framing

These points recur across the source and matter directly for iOS code audits:

### A. Platform accessibility services are central

WCAG2ICT repeatedly emphasizes that software programmatic determinability is typically achieved via platform accessibility services.

iOS translation:

- Prefer evidence from standard `UIKit` / `SwiftUI` controls and accessibility APIs.
- Treat custom controls as higher risk and inspect explicit semantics (`name`, `role/traits`, `state/value`, notifications/actions).

### B. Many mobile SC applications are "direct as written"

For many SCs, WCAG2Mobile/WCAG2ICT mainly says the SC applies directly (sometimes with terminology substitutions).

iOS translation:

- Do not wait for mobile-specific prose if the requirement is clear in WCAG.
- Audit against the SC directly and use iOS APIs/patterns as evidence.

### C. Placeholder sections do not reduce audit obligation

If the WCAG2Mobile section is still placeholder:

- continue auditing the SC using WCAG 2.2 + WCAG2ICT + iOS platform evidence.

### D. Code-only audit limitation must be explicit

Some outcomes remain code-indeterminate (contrast, rendered target size, VoiceOver output order/timing, visible focus indicator quality).

In this skill:

- mark these as `Needs user verification`
- provide a concrete manual check for the user

## Priority SC Reference (Mobile-Heavy)

This section summarizes what is materially useful from the source for the mobile-heavy SCs prioritized by the skill.

### SC 1.3.4 Orientation (AA)

WCAG2Mobile draft status:

- Has non-placeholder mobile text (useful)

What is retained from the source (distilled):

- Applies directly as written.
- WCAG2Mobile adds a practical best-practice note: support all available orientations (including reversed portrait/landscape) where available.

iOS audit implication:

- Treat orientation lock decisions as feature-level design constraints that require justification.
- Code evidence can show locks and assumptions; usability across orientations may still require user verification.

Use in findings:

- Cite orientation-lock code or per-screen orientation constraints.
- If no clear essential reason is visible in code, flag as likely issue or `Needs user verification` depending on evidence strength.

### SC 1.4.10 Reflow (AA)

WCAG2Mobile draft status:

- WCAG2ICT adaptation is detailed; WCAG2Mobile section itself is still placeholder/WIP

What is retained from the source (distilled):

- Apply the SC to non-web software content with reflow intent preserved.
- WCAG2ICT emphasizes reflow when users scale content, resize windows/dialogs/content areas, or change resolution.
- Two-dimensional layout exceptions still exist (for interfaces/content that genuinely require it).
- If exact platform dimensions are not supported, evaluate at the nearest practical size and document that limitation.

iOS audit implication:

- For iOS code review, inspect for layout rigidity and text scaling breakage signals (fixed sizes, truncation, narrow-width fragility).
- Avoid claiming `Pass` from code alone unless layout behavior is directly provable.

Use in findings:

- Combine code evidence (fixed widths/heights, `lineLimit(1)`, non-scaling typography) with a user follow-up check for large text + narrow width/orientation.

### SC 2.5.1 Pointer Gestures (A)

WCAG2Mobile draft status:

- WCAG2ICT adaptation present; WCAG2Mobile section is placeholder/WIP

What is retained from the source (distilled):

- Applies to functionality implemented by the application/content layer that interprets pointer actions.
- Does not apply to gestures required to operate the underlying platform or assistive technology.

iOS audit implication:

- Audit app-defined gestures (`Swipe`, `DragGesture`, custom recognizers), not OS-level gestures.
- Require a single-pointer non-path alternative unless the gesture is essential.

Use in findings:

- Be explicit that the issue is in app-level gesture handling, not iOS system gestures.

### SC 2.5.4 Motion Actuation (A)

WCAG2Mobile draft status:

- Non-placeholder (direct application)

What is retained from the source (distilled):

- Applies directly as written.

iOS audit implication:

- If feature code uses shake/tilt/motion, look for equivalent UI controls and an option to prevent accidental actuation where applicable.

Use in findings:

- Strong code evidence if motion handlers exist without alternative UI paths.

### SC 2.5.7 Dragging Movements (AA)

WCAG2Mobile draft status:

- WCAG2ICT adaptation present; WCAG2Mobile section is placeholder/WIP

What is retained from the source (distilled):

- Applies to dragging functionality implemented by the application/content layer.
- WCAG2ICT adapts the user-agent wording for non-web contexts and keeps the same core requirement: non-drag single-pointer alternative unless dragging is essential.

iOS audit implication:

- Audit custom reordering, draggable controls, slider-like drag interactions, and pan-gesture driven operations.
- Look for explicit alternatives (move up/down, plus/minus, menu actions).

Use in findings:

- Distinguish `drag present` from `drag required`; the failure is absence of equivalent non-drag operation.

### SC 2.5.8 Target Size (Minimum) (AA)

WCAG2Mobile draft status:

- WCAG2ICT adaptation is detailed; WCAG2Mobile section is placeholder/WIP

What is retained from the source (distilled):

- WCAG2ICT adapts terminology for non-web contexts, including:
  - equivalent control availability in the same software/document context,
  - user-agent/platform-software controlled target sizes,
  - CSS pixel interpretation notes for non-web contexts.
- Core exceptions remain (spacing, equivalent control, inline, platform-controlled, essential/legal).

iOS audit implication:

- Code review can identify target-size risk patterns (small icon-only buttons, dense controls, no padding/hit-area expansion).
- Final measurements usually require user verification unless rendered sizes are directly derivable.

Use in findings:

- Reference exception logic carefully (especially `Equivalent`), and ensure the equivalent control is truly in the same feature context and provides the same function.

### SC 3.3.7 Redundant Entry (A)

WCAG2Mobile draft status:

- Non-placeholder (direct application)

What is retained from the source (distilled):

- Applies directly as written.

iOS audit implication:

- Evaluate multi-screen processes for reused/prefilled/selectable values.
- Common code evidence: dropped state, repeated field reconstruction, missing persisted form model.

Use in findings:

- Flag repeated entry in the same process unless essential/security/invalidity exceptions are clearly applicable.

### SC 3.3.8 Accessible Authentication (Minimum) (AA)

WCAG2Mobile draft status:

- Has meaningful mobile-specific text (useful)

What is retained from the source (distilled):

- WCAG2ICT applies the SC to software contexts with non-web substitutions.
- WCAG2Mobile further adapts wording toward mobile `view` contexts.
- Source explicitly preserves the examples of helpful mechanisms such as:
  - password manager support
  - copy/paste support
- Source notes that passwords used to unlock underlying platform software are outside the app author's scope.

iOS audit implication:

- Prioritize auth flows (`login`, MFA, OTP) for paste blocking, autofill friction, fragmented OTP entry semantics, and memory-dependent requirements.
- Distinguish app-authentication requirements from device unlock requirements.

Use in findings:

- Strong signal: disabled paste or hostile OTP implementations.
- Mention app-vs-platform scope boundary to avoid false positives.

## Core iOS UI SC Reference

These SCs are central to iOS code audits even when WCAG2Mobile draft text is still incomplete.

### SC 1.1.1 Non-text Content (A)

WCAG2Mobile draft status:

- Has a small mobile-specific note (useful)

What is retained from the source (distilled):

- Applies directly as written.
- WCAG2Mobile adds that not all mobile platforms provide a way to programmatically associate a label with non-text content.

iOS audit implication:

- Prefer native controls/components that expose accessible names cleanly.
- Inspect icon-only controls and informative images carefully.

### SC 1.3.1 Info and Relationships (A)

WCAG2Mobile draft status:

- Placeholder/WIP, but WCAG2ICT note is useful

What is retained from the source (distilled):

- WCAG2ICT notes that software programmatic determinability is best achieved via platform accessibility services.

iOS audit implication:

- Inspect heading semantics, grouping, label-value relationships, and composite controls using platform accessibility APIs/modifiers.

### SC 2.4.2 Page Titled (A) in mobile context (screen identification)

WCAG2Mobile draft status:

- Placeholder/WIP, but WCAG2ICT notes are useful

What is retained from the source (distilled):

- WCAG2ICT substitutes software/document titles for page titles.
- WCAG2ICT also notes that individual windows/screens having descriptive titles is best practice, even where not strictly required by this SC.

iOS audit implication:

- Audit screen identity via navigation titles/headings/context text and screen-change announcements when needed.

### SC 2.4.3 Focus Order (A)

WCAG2Mobile draft status:

- Placeholder/WIP

What is retained from the source (distilled):

- Direct applicability concept carries over: sequential focus/navigation order must preserve meaning and operability.

iOS audit implication:

- Review custom containers, manual `accessibilityElements`, modal presentation focus handoff, and composite control ordering.

### SC 2.4.7 Focus Visible (AA)

WCAG2Mobile draft status:

- Placeholder/WIP (direct application framing)

What is retained from the source (distilled):

- Apply directly for keyboard-operable UI modes.

iOS audit implication:

- Relevant for external keyboard / Switch Control pathways and some focus-based navigation contexts.
- Usually requires user verification for final visual result.

### SC 2.4.11 Focus Not Obscured (Minimum) (AA)

WCAG2Mobile draft status:

- Placeholder/WIP (direct application framing)

What is retained from the source (distilled):

- Apply directly: author-created content should not fully hide the focused component.

iOS audit implication:

- Audit keyboard/focus movement around sticky UI, bottom sheets, and keyboard overlays.
- Final behavior typically needs user verification.

### SC 2.5.3 Label in Name (A)

WCAG2Mobile draft status:

- Non-placeholder (direct application)

What is retained from the source (distilled):

- Applies directly as written.
- WCAG best-practice note remains useful: label text at the start of the accessible name is preferable.

iOS audit implication:

- Compare visible button text to `.accessibilityLabel` overrides.
- Avoid replacing visible action words with different phrasing unless the visible text is preserved in the name.

### SC 4.1.2 Name, Role, Value (A)

WCAG2Mobile draft status:

- Placeholder/WIP, but WCAG2ICT notes are highly useful

What is retained from the source (distilled):

- WCAG2ICT reframes this SC for software developers using custom controls.
- WCAG2ICT strongly recommends using platform accessibility services for interoperability.
- Standard platform controls usually satisfy much of this when used correctly; custom controls are the main risk area.

iOS audit implication:

- Treat custom `UIView` / custom composite controls as high priority.
- Audit for programmatic name, role/traits, state/value, and change notifications/actions.

### SC 4.1.3 Status Messages (AA)

WCAG2Mobile draft status:

- Has meaningful mobile-specific text (useful)

What is retained from the source (distilled):

- WCAG2ICT clarifies the user need remains even outside markup-based content.
- WCAG2Mobile explicitly removes the web/markup limitation in practice for mobile content interpretation.
- Programmatic exposure of status messages should be implemented through user-agent/platform accessibility services so AT can present them without moving focus.

iOS audit implication:

- Audit success/error/progress/loading messages for announcement paths (for example via `UIAccessibility.post(...)`), while confirming code path relevance.

Use in findings:

- Distinguish "message exists visually" from "message is programmatically exposed without forced focus change".

## Practical Use in This Skill

When using this file during an audit:

1. Use it to interpret scope and terminology (`screen`, `set of screens`, informative vs normative).
2. Check each SC's draft maturity (`useful mobile-specific text` vs `placeholder/WIP`).
3. If placeholder/WIP, rely on:
   - WCAG 2.2 SC intent,
   - WCAG2ICT adaptation notes summarized here,
   - iOS API evidence from `ios-accessibility-api-examples.md`.
4. In reports, state uncertainty clearly when final behavior is code-indeterminate.

## Source Provenance

Primary source used to build this distilled reference:

- `/Users/romanmirzoyan/Developer/a11y-skill/wcag_doc.md`

If exact wording is disputed, consult the source file directly and quote only the specific line(s) needed for that dispute.
