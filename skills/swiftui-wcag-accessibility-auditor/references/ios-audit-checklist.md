# iOS Accessibility Audit Checklist (WCAG 2.2 + WCAG2Mobile Interpretation)

## Table of Contents

- How to Use This Checklist
- iOS-First Triage
- Priority SCs (Mobile-Heavy)
- Core Semantics and Operability SCs
- Forms, Errors, and Authentication SCs
- Visual and Adaptation SCs
- User Follow-Up Check Prompts (Reusable)
- Coverage Matrix Minimum Scope

## How to Use This Checklist

Use this checklist for code inspection of native iOS features only (`SwiftUI` / `UIKit`).

For each success criterion (SC):

1. Inspect the listed code signals.
2. Record evidence from actual feature code.
3. Mark status in the coverage matrix.
4. If code cannot prove behavior, mark `Needs user verification` and add a user follow-up check.

Use `references/ios-accessibility-api-examples.md` when you need concrete API examples.

## iOS-First Triage

Run this fast pass before the full checklist:

1. Locate the entry screen and downstream states (`sheet`, modal, error, success).
2. Find icon-only controls and custom `UIView` / gesture-based controls.
3. Find semantic hooks:
   - SwiftUI accessibility modifiers
   - UIKit `isAccessibilityElement`, labels, traits, values
   - `UIAccessibility.post(...)`
4. Find Dynamic Type risks:
   - fixed frames/heights
   - `lineLimit(1)` in critical labels
   - fixed font sizes without scaling
5. Find gesture-only or drag-based interactions.
6. Build the SC coverage matrix.

## Priority SCs (Mobile-Heavy)

Start with these for most iOS feature audits.

### SC 1.3.4 Orientation (AA)

Inspect:

- orientation locks in app/scene/view-controller code
- per-screen orientation overrides
- feature logic that assumes portrait-only layouts

Common failures:

- forcing one orientation for convenience instead of essential need
- layout code that only works in one orientation

User follow-up check (if needed):

- Rotate to portrait/landscape and verify the feature remains usable without hidden or clipped controls.

### SC 1.4.10 Reflow (AA)

Inspect:

- hard-coded widths/heights in key containers
- truncation-prone labels in primary tasks
- stack/layout code that does not adapt to narrower widths

Common failures:

- horizontal scrolling introduced by fixed-width content in task flows
- clipped content at larger text + narrow width combinations

User follow-up check (if needed):

- Use largest text size and landscape/narrow width; confirm content and controls remain usable without horizontal scrolling (except allowed cases).

### SC 2.5.1 Pointer Gestures (A)

Inspect:

- custom gestures (`onTapGesture`, swipe, multi-step gestures)
- gesture recognizers on essential actions
- whether an equivalent control (`Button`, menu action) exists

Common failures:

- swipe-only archive/delete/reveal actions with no visible alternative
- path-based gestures required for core tasks

User follow-up check (if needed):

- Verify every gesture-driven action has an equivalent single-pointer UI control.

### SC 2.5.4 Motion Actuation (A)

Inspect:

- motion/shake/tilt handlers
- feature code relying on device movement for commands
- availability of explicit UI alternatives

Common failures:

- shake to undo/action without equivalent button or menu action

User follow-up check (if needed):

- Confirm a non-motion UI path exists for each motion-triggered action.

### SC 2.5.7 Dragging Movements (AA)

Inspect:

- `DragGesture`, `UIPanGestureRecognizer`, drag/reorder controls
- custom sliders/reorder UIs
- alternate actions (move up/down, increment/decrement)

Common failures:

- drag-only reordering in lists
- custom draggable controls without step-based alternatives

User follow-up check (if needed):

- Verify drag tasks can be completed with a non-drag alternative unless dragging is essential.

### SC 2.5.8 Target Size (Minimum) (AA)

Inspect:

- small icon-only tappable areas
- dense rows of controls
- padding/content shape/hit area expansion
- custom touch handling in small bounds

Common failures:

- visible icon is also the full hit target with no padding
- tightly packed controls with insufficient spacing

User follow-up check (if needed):

- Measure rendered target sizes/spacing for small controls in the feature.

### SC 3.3.7 Redundant Entry (A)

Inspect:

- multi-step forms/workflows
- state persistence across screens
- whether previously entered values are reused/prefilled/selectable

Common failures:

- repeated user entry due to dropped state between steps
- asking for the same information again without reuse

User follow-up check (if needed):

- Complete the flow and verify repeated data is reused or selectable.

### SC 3.3.8 Accessible Authentication (Minimum) (AA)

Inspect:

- login/MFA/OTP flows
- paste restrictions
- custom OTP fields and focus behavior code
- support for autofill/password manager hooks (where applicable)

Common failures:

- blocking paste in password or OTP fields
- OTP inputs that fragment entry and break accessibility navigation
- memorization/cognitive test patterns without alternatives

User follow-up check (if needed):

- Verify paste and password manager/OTP autofill paths work in the auth flow.

## Core Semantics and Operability SCs

### SC 1.1.1 Non-text Content (A)

Inspect:

- icon-only buttons
- informative images/status icons
- decorative images hidden from accessibility

Common failures:

- meaningful image/icon without accessible name
- decorative image announced unnecessarily

### SC 1.3.1 Info and Relationships (A)

Inspect:

- label-field associations
- grouped controls and headings
- semantic grouping in custom composite views

Common failures:

- visually grouped elements implemented as unrelated accessible nodes
- missing heading semantics for section titles

### SC 2.1.1 Keyboard (A) and SC 2.1.2 No Keyboard Trap (A)

Inspect:

- focus movement code for modals/custom controls
- responder/focus handling in text input flows
- custom input views and accessory controls

Common failures:

- modal/custom control focus gets stuck
- no path to dismiss/leave a focused interactive region

User follow-up check (if needed):

- Use external keyboard or Switch Control to navigate into and out of custom controls/modals.

### SC 2.4.2 Page Titled (A) in Mobile Context (Screen Identification)

Inspect:

- navigation titles / screen labels
- view-controller titles and heading text
- context change announcements where needed

Common failures:

- screens without clear identifying title/context

### SC 2.4.3 Focus Order (A)

Inspect:

- custom accessibility container ordering
- modal/sheet focus target setup
- composite views with manual `accessibilityElements`

Common failures:

- illogical reading/focus order in custom containers
- focus jumps to background elements after modal presentation

User follow-up check (if needed):

- With VoiceOver, verify navigation order follows the visual/task order.

### SC 2.4.7 Focus Visible (AA) and SC 2.4.11 Focus Not Obscured (Minimum) (AA)

Inspect:

- custom focus styling code (if any)
- scroll-to-field behavior when focus/input changes
- overlays/headers that could cover focused elements

Common failures:

- focused field hidden behind keyboard or sticky chrome
- focus indicator suppressed/unclear in custom components

User follow-up check (if needed):

- Navigate with external keyboard/Switch Control and confirm focused elements are visible and not obscured.

### SC 2.5.3 Label in Name (A)

Inspect:

- visible button text vs `.accessibilityLabel`
- custom labels that replace visible text with different spoken text

Common failures:

- visible text "Continue" but accessibility label omits/replaces "Continue"

### SC 4.1.2 Name, Role, Value (A)

Inspect:

- custom `UIView` controls
- SwiftUI custom composites with manual accessibility modifiers
- control state/value exposure (`selected`, `expanded`, counts, slider values)

Common failures:

- tappable custom view missing `isAccessibilityElement`
- missing trait/role/state/value on custom controls

### SC 4.1.3 Status Messages (AA)

Inspect:

- success/error banners
- toasts/snackbars
- loading completion messages
- announcement posting code (`UIAccessibility.post`)

Common failures:

- visual status changes with no announcement path
- announcement helper exists but is not called in the real feature path

User follow-up check (if needed):

- Trigger the status change with VoiceOver and confirm the message is announced once and at the right time.

## Forms, Errors, and Authentication SCs

### SC 1.3.5 Identify Input Purpose (AA)

Inspect:

- text-field configuration for common input purposes
- autofill-related content types/keyboard types (email, phone, one-time code, etc.)

Common failures:

- common-purpose fields missing input-purpose hints

### SC 3.3.1 Error Identification (A)

Inspect:

- validation flow code
- where error messages are rendered and attached to fields/forms

Common failures:

- field enters error state visually with no readable error text

### SC 3.3.2 Labels or Instructions (A)

Inspect:

- text fields relying on placeholder-only labeling
- required-format instructions (date, password, code)

Common failures:

- placeholder used as sole label
- no instructions for constrained formats

### SC 3.3.3 Error Suggestion (AA)

Inspect:

- validation messaging content
- branch-specific error handling

Common failures:

- generic error without correction guidance when suggestions are possible

### SC 3.3.4 Error Prevention (Legal, Financial, Data) (AA) when applicable

Inspect:

- destructive or high-impact submissions
- review/confirm flows
- undo or correction paths

Common failures:

- high-impact submission with no review/confirmation/correction path

## Visual and Adaptation SCs

### SC 1.4.3 Contrast (Minimum) (AA)

Code-only guidance:

- Flag likely low-contrast tokens, alpha overlays, disabled-text styling, or subtle borders.
- Do not assert `Pass` from code alone unless values and computed contrast are clearly available and checked.

User follow-up check (if needed):

- Measure text contrast for primary, secondary, and error text styles used in the feature.

### SC 1.4.4 Resize Text (AA)

Inspect:

- Dynamic Type support in UIKit
- scalable text styles in SwiftUI
- truncation/clip risk in critical actions and labels

Common failures:

- fixed-size text in task-critical UI
- large-text clipping caused by fixed-height containers

User follow-up check (if needed):

- Enable largest text size and verify task completion remains possible.

### SC 1.4.11 Non-text Contrast (AA)

Code-only guidance:

- Flag low-contrast focus indicators, control outlines, and state indicators.
- Treat final pass/fail as `Needs user verification` unless rendered values are proven.

User follow-up check (if needed):

- Measure contrast for control boundaries, selected states, and focus indicators.

## User Follow-Up Check Prompts (Reusable)

Reuse these prompt shapes when code is inconclusive:

- "With VoiceOver on, perform `<action>` on `<screen>` and confirm `<announcement/order>`."
- "At the largest text size, open `<screen>` and confirm `<label/control>` remains visible and usable."
- "Measure the tap target/spacing of `<control>` on `<screen>`."
- "Rotate the device on `<screen>` and confirm `<task>` remains possible."
- "Use external keyboard or Switch Control on `<screen>` and confirm focus can move to and from `<control>`."

## Coverage Matrix Minimum Scope

Include at least:

- mobile-heavy SCs: `1.3.4`, `1.4.10`, `2.5.1`, `2.5.4`, `2.5.7`, `2.5.8`, `3.3.7`, `3.3.8`
- core iOS UI SCs: `1.1.1`, `1.3.1`, `2.4.2`, `2.4.3`, `2.4.7`, `2.4.11`, `2.5.3`, `4.1.2`, `4.1.3`
- forms/auth SCs when relevant: `1.3.5`, `3.3.1`, `3.3.2`, `3.3.3`, `3.3.4`
