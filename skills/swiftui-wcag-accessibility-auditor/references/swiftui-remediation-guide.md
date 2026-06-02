# SwiftUI Remediation Guide (Patch-Ready)

## Table of Contents

- Purpose
- Non-Goals
- Priority Model (P0/P1/P2)
- Patch Style Rules
- Common Fix Patterns (SwiftUI)
- User Follow-Up Checks (When Code Is Not Enough)

## Purpose

Use this file after identifying WCAG issues to produce minimal, patch-ready SwiftUI fixes.

This file is not a replacement for the WCAG checklist. Use it to turn findings into code changes without drifting into unnecessary refactors.

## Non-Goals

- Do not rewrite whole screens for style consistency.
- Do not add redundant accessibility modifiers when built-in semantics are already correct.
- Do not change visible copy unless accessibility requires it.
- Do not introduce architecture changes unless a WCAG blocker cannot be fixed locally.

## Priority Model (P0/P1/P2)

Use this for remediation ordering in the merged skill:

- `P0`: likely blocks or seriously degrades task completion for assistive tech users in the scoped flow
- `P1`: significant accessibility issue with a workaround or narrower scope
- `P2`: improvement or lower-risk issue, but still worth fixing

Map from WCAG evidence pragmatically:

- `Fail` on core control semantics, auth flow barriers, or missing status announcements in key flows -> usually `P0` or `P1`
- `Needs user verification` items are not findings by default; only assign `P*` if code strongly indicates a likely issue

## Patch Style Rules

- Prefer the smallest code change that fixes the issue.
- Preserve visible text and interaction model unless the interaction itself violates WCAG.
- Explain why each added modifier/API matters.
- Prefer `accessibilityHint` over replacing visible text with a different `accessibilityLabel` when possible.
- For `Label in Name` (`2.5.3`), keep visible text inside the accessible name.
- If proposing grouping changes, explain the announcement/read-order tradeoff.
- When code cannot prove the final result, state that and add a user follow-up check.

## Common Fix Patterns (SwiftUI)

### [SwiftUI] 1. Icon-only button missing accessible name

Problem signal:

```swift
Button {
    refresh()
} label: {
    Image(systemName: "arrow.clockwise")
}
```

Patch direction:

```swift
Button {
    refresh()
} label: {
    Image(systemName: "arrow.clockwise")
}
.accessibilityLabel("Refresh")
.accessibilityHint("Reloads the content")
```

Common SC mapping:

- `1.1.1`
- `4.1.2`

### [SwiftUI] 2. Visible text replaced with different spoken label (Label in Name risk)

Problem signal:

```swift
Button("Continue") {
    submit()
}
.accessibilityLabel("Proceed to next step")
```

Patch direction (preserve visible text in name):

```swift
Button("Continue") {
    submit()
}
.accessibilityHint("Submits your information and moves to the next step")
```

Common SC mapping:

- `2.5.3`

### [SwiftUI] 3. Tap gesture on non-button container (semantic/operability risk)

Problem signal:

```swift
HStack {
    Text("Email")
    Text(user.email)
}
.onTapGesture { editEmail() }
```

Patch direction (prefer semantic control):

```swift
Button {
    editEmail()
} label: {
    HStack {
        Text("Email")
        Text(user.email)
    }
}
```

Audit note:

- If visual behavior must remain custom, add explicit semantics and justify why a `Button` cannot be used.

Common SC mapping:

- `4.1.2`
- `1.3.1` (depending on grouping/structure)

### [SwiftUI] 4. Heading not exposed as header

Problem signal:

```swift
Text("Billing address")
    .font(.headline)
```

Patch direction:

```swift
Text("Billing address")
    .font(.headline)
    .accessibilityAddTraits(.isHeader)
```

Common SC mapping:

- `1.3.1`

### [SwiftUI] 5. Fixed-size/truncating text in critical UI (Dynamic Type / Reflow risk)

Problem signal:

```swift
Text(viewModel.primaryActionTitle)
    .font(.system(size: 14))
    .lineLimit(1)
    .frame(height: 32)
```

Patch direction (example):

```swift
Text(viewModel.primaryActionTitle)
    .font(.headline)
    .lineLimit(2)
    .padding(.vertical, 12)
```

Audit note:

- Do not assert full pass from code alone if rendered behavior remains uncertain.

Common SC mapping:

- `1.4.4`
- `1.4.10`

### [SwiftUI] 6. Small tap target risk

Problem signal:

```swift
Button {
    close()
} label: {
    Image(systemName: "xmark")
}
```

Patch direction:

```swift
Button {
    close()
} label: {
    Image(systemName: "xmark")
        .padding(12)
        .contentShape(Rectangle())
}
```

Common SC mapping:

- `2.5.8`

### [SwiftUI] 7. Drag-only operation with no alternate control

Problem signal:

```swift
ReorderHandle()
    .gesture(DragGesture().onChanged { _ in })
```

Patch direction (add equivalent controls):

```swift
HStack {
    Button("Move up") { viewModel.moveItemUp(id) }
    Button("Move down") { viewModel.moveItemDown(id) }
}

ReorderHandle()
    .gesture(DragGesture().onChanged { _ in })
```

Common SC mapping:

- `2.5.7`
- `2.5.1` (if the gesture is path-based/complex)

### [SwiftUI] 8. Focus target not established when presenting important state

Problem signal:

- Modal/error sheet appears with no clear initial accessibility focus target.

Patch direction (example):

```swift
struct ErrorSheet: View {
    @AccessibilityFocusState private var isTitleFocused: Bool

    var body: some View {
        VStack(alignment: .leading) {
            Text("Payment failed")
                .font(.title2)
                .accessibilityAddTraits(.isHeader)
                .accessibilityFocused($isTitleFocused)
            Text("Try another card or check your billing address.")
        }
        .onAppear { isTitleFocused = true }
    }
}
```

Common SC mapping:

- `2.4.3`
- sometimes `4.1.3` (depending on message behavior)

### [SwiftUI] 9. Motion-heavy animation ignoring Reduce Motion

Problem signal:

- Core feedback/transition depends on animation and no reduced-motion path is visible.

Patch direction (example pattern):

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

withAnimation(reduceMotion ? nil : .spring()) {
    isExpanded.toggle()
}
```

Common SC mapping:

- `2.5.4` (when motion actuation is involved)
- usability/accessibility quality improvement even when no direct WCAG failure is proven from code

## User Follow-Up Checks (When Code Is Not Enough)

Add user follow-up checks instead of guessing for:

- final VoiceOver reading order/announcements
- visual focus visibility / focus not obscured
- contrast ratios
- rendered tap target size/spacing
- large text clipping/reflow outcomes
- orientation usability

Use `references/swiftui-manual-checklist.md` as the base and tailor checks to the scoped screen.
