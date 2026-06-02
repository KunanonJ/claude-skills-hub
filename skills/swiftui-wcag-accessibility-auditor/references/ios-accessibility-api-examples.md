# iOS Accessibility API Examples (SwiftUI + UIKit)

## Table of Contents

- How to Use This File
- SwiftUI: Semantics and Naming
- SwiftUI: Grouping, Headings, and Label-in-Name
- SwiftUI: Gestures, Dragging, and Alternatives
- SwiftUI: Dynamic Type and Layout Risk Signals
- SwiftUI: Target Size Risk Signals
- UIKit: Semantics and Custom Controls
- UIKit: Focus, Modal Context, and Announcements
- UIKit: Dynamic Type and Input Purpose Signals
- Search Cheatsheet (iOS Only)

## How to Use This File

Use these snippets to improve code-audit accuracy:

- flag common anti-patterns quickly
- recognize positive evidence without over-claiming a pass
- map APIs to likely WCAG criteria

These snippets are examples, not mandatory implementations.

## SwiftUI: Semantics and Naming

### [SwiftUI] Icon-only button without accessible name (flag)

```swift
Button {
    viewModel.refresh()
} label: {
    Image(systemName: "arrow.clockwise")
}
```

Likely concerns:

- `1.1.1` Non-text Content
- `4.1.2` Name, Role, Value

### [SwiftUI] Icon-only button with explicit accessible name (positive evidence)

```swift
Button {
    viewModel.refresh()
} label: {
    Image(systemName: "arrow.clockwise")
}
.accessibilityLabel("Refresh")
.accessibilityHint("Reloads the content")
```

### [SwiftUI] Decorative image hidden from accessibility (positive evidence)

```swift
Image("confetti-background")
    .resizable()
    .accessibilityHidden(true)
```

Use this when the image is purely decorative and adds no information.

### [SwiftUI] Meaningful status icon with weak semantics (review grouping)

```swift
HStack {
    Image(systemName: "exclamationmark.triangle.fill")
    Text("Payment issue")
}
```

Audit note:

- If the icon adds meaning beyond the text, confirm the combined accessible output conveys that meaning.
- Check grouping/children behavior instead of assuming the default is correct.

## SwiftUI: Grouping, Headings, and Label-in-Name

### [SwiftUI] Section title marked as heading (positive evidence)

```swift
Text("Billing address")
    .font(.headline)
    .accessibilityAddTraits(.isHeader)
```

Relevant SCs:

- `1.3.1`

### [SwiftUI] Composite row flattened incorrectly (flag risk)

```swift
HStack {
    Text("Email")
    Text(user.email)
}
.onTapGesture { editEmail() }
```

Audit note:

- Gesture on a non-button container often needs semantic review.
- Check whether the row exposes role/name/action clearly (`4.1.2`).

### [SwiftUI] Visible text and accessibility label mismatch (label-in-name risk)

```swift
Button("Continue") {
    submit()
}
.accessibilityLabel("Proceed to next step")
```

Likely concern:

- `2.5.3` Label in Name (voice-control compatibility risk)

Safer direction:

```swift
Button("Continue") {
    submit()
}
.accessibilityHint("Submits your information and moves to the next step")
```

### [SwiftUI] Overriding child semantics accidentally (review carefully)

```swift
VStack(alignment: .leading) {
    Text("Payment method")
    Text(maskedCardNumber)
}
.accessibilityElement(children: .ignore)
.accessibilityLabel("Card")
```

Audit note:

- `.ignore` can hide useful child semantics/value text if not rebuilt fully.
- Check for loss of visible text in the final accessible name/value.

## SwiftUI: Gestures, Dragging, and Alternatives

### [SwiftUI] Swipe/gesture-only action pattern (flag)

```swift
MessageRow(message)
    .onTapGesture { openMessage(message) }
    .gesture(
        DragGesture(minimumDistance: 20)
            .onEnded { value in
                if value.translation.width < -60 {
                    archive(message)
                }
            }
    )
```

Audit questions:

- Is there a visible `Button`/menu alternative for archive?
- Is the drag/swipe action essential?

Relevant SCs:

- `2.5.1`
- `2.5.7`

### [SwiftUI] Drag interaction with explicit alternatives (positive evidence)

```swift
HStack {
    Button("Move up") { viewModel.moveItemUp(id) }
    Button("Move down") { viewModel.moveItemDown(id) }
}

ReorderHandle()
    .gesture(DragGesture().onChanged { _ in })
```

Audit note:

- Presence of drag plus explicit move controls is good evidence for `2.5.7`, but confirm the controls apply to the same operation.

## SwiftUI: Dynamic Type and Layout Risk Signals

### [SwiftUI] Fixed-size text and single-line truncation in critical UI (flag risk)

```swift
Text(viewModel.primaryActionTitle)
    .font(.system(size: 14, weight: .semibold))
    .lineLimit(1)
    .frame(height: 32)
```

Likely concerns:

- `1.4.4` Resize Text
- `1.4.10` Reflow

Audit note:

- This is not an automatic failure from code alone. Mark `Needs user verification` if rendering outcome is unknown.

### [SwiftUI] Scalable typography with flexible layout (positive evidence)

```swift
Text(viewModel.primaryActionTitle)
    .font(.headline)
    .lineLimit(2)
    .multilineTextAlignment(.center)
    .padding(.vertical, 12)
```

Positive evidence for:

- Dynamic Type readiness (not proof of full pass)

### [SwiftUI] Accessibility focus for modal entry point (positive evidence)

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
        .onAppear {
            isTitleFocused = true
        }
    }
}
```

Relevant SCs:

- `2.4.3`
- `4.1.3` (depending on surrounding messaging)

## SwiftUI: Target Size Risk Signals

### [SwiftUI] Small tappable icon without padding (flag risk)

```swift
Button {
    close()
} label: {
    Image(systemName: "xmark")
}
```

Likely concern:

- `2.5.8` Target Size (Minimum)

### [SwiftUI] Expanded hit area (positive evidence)

```swift
Button {
    close()
} label: {
    Image(systemName: "xmark")
        .padding(12)
        .contentShape(Rectangle())
}
```

Audit note:

- Still treat final target-size result as code-indeterminate unless rendered size is provable.

## UIKit: Semantics and Custom Controls

### [UIKit] Custom interactive view with no accessibility semantics (flag)

```swift
final class RatingDotsView: UIView {
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        updateRatingFromTouch(touches)
    }
}
```

Likely concern:

- `4.1.2` Name, Role, Value

### [UIKit] Custom adjustable control with semantics (positive evidence)

```swift
final class RatingDotsView: UIView {
    private var rating: Int = 3 {
        didSet { accessibilityValue = "\(rating) of 5" }
    }

    override init(frame: CGRect) {
        super.init(frame: frame)
        isAccessibilityElement = true
        accessibilityTraits = [.adjustable]
        accessibilityLabel = "Rating"
        accessibilityValue = "\(rating) of 5"
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    override func accessibilityIncrement() { rating = min(5, rating + 1) }
    override func accessibilityDecrement() { rating = max(1, rating - 1) }
}
```

Relevant SCs:

- `4.1.2`
- `2.5.7` (if replacing a drag-only adjustment)

### [UIKit] Custom actions for complex rows (positive evidence)

```swift
accessibilityCustomActions = [
    UIAccessibilityCustomAction(name: "Archive", target: self, selector: #selector(archiveMessage)),
    UIAccessibilityCustomAction(name: "Mark as unread", target: self, selector: #selector(markUnread))
]
```

Audit note:

- This can support alternatives to gesture-only actions, but confirm parity with visible UI behavior.

## UIKit: Focus, Modal Context, and Announcements

### [UIKit] Modal context isolation clue (positive evidence)

```swift
modalContainerView.accessibilityViewIsModal = true
```

Relevant SCs:

- `2.4.3`
- `2.1.2`

### [UIKit] Explicit focus change on screen/modal update (positive evidence)

```swift
UIAccessibility.post(notification: .screenChanged, argument: titleLabel)
```

Use as evidence for focus management intent. Do not assume it works correctly without manual observation.

### [UIKit] Status message announcement (positive evidence; verify call path)

```swift
UIAccessibility.post(notification: .announcement, argument: "Payment method saved")
```

Relevant SC:

- `4.1.3`

Audit note:

- Confirm this is triggered in the real success/error branch of the audited flow.

### [UIKit] Manual accessibility container order (review carefully)

```swift
override var accessibilityElements: [Any]? {
    get { [titleLabel, subtitleLabel, amountLabel, actionButton] }
    set { }
}
```

Audit note:

- Manual ordering can fix or create `2.4.3` issues. Review the order against task flow.

## UIKit: Dynamic Type and Input Purpose Signals

### [UIKit] Dynamic Type support evidence (positive, not full proof)

```swift
titleLabel.font = UIFont.preferredFont(forTextStyle: .headline)
titleLabel.adjustsFontForContentSizeCategory = true
```

Relevant SCs:

- `1.4.4`
- `1.4.10`

### [UIKit] Fixed-size typography in critical UI (flag risk)

```swift
titleLabel.font = UIFont.systemFont(ofSize: 14, weight: .semibold)
titleLabel.adjustsFontForContentSizeCategory = false
```

Likely concern:

- Dynamic Type support absent or weakened in important content

### [UIKit] Input purpose signals (use as evidence for `1.3.5`)

```swift
emailField.keyboardType = .emailAddress
emailField.textContentType = .emailAddress

otpField.keyboardType = .numberPad
otpField.textContentType = .oneTimeCode

passwordField.textContentType = .password
```

Audit note:

- Input-purpose hints support autofill and reduce auth friction; still audit the full auth flow for `3.3.8`.

## Search Cheatsheet (iOS Only)

Use `rg` with the scoped feature path first, then broaden if needed.

```bash
rg -n "accessibility(Label|Hint|Value)|accessibility(AddTraits|RemoveTraits)|accessibilityHidden" .
rg -n "UIAccessibility|isAccessibilityElement|accessibilityTraits|accessibilityElements|accessibilityViewIsModal" .
rg -n "UIAccessibility\\.post|\\.announcement|\\.screenChanged|\\.layoutChanged" .
rg -n "@AccessibilityFocusState|accessibilityFocused\\(" .
rg -n "UIFontMetrics|preferredFont\\(forTextStyle:|adjustsFontForContentSizeCategory|dynamicTypeSize" .
rg -n "textContentType|keyboardType|oneTimeCode" .
rg -n "onTapGesture|DragGesture|UIPanGestureRecognizer|UISwipeGestureRecognizer" .
```
