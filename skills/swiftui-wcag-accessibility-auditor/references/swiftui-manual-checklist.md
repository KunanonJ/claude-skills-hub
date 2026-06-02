# SwiftUI Manual Accessibility Checklist (iOS Follow-Up)

Use this checklist only for user follow-up checks when the code audit cannot prove the behavior.

## VoiceOver and Semantics

- [ ] All icon-only buttons have a clear, meaningful label
- [ ] No duplicated announcements (parent + child reading the same content)
- [ ] Headers are exposed as headers where they structure the screen
- [ ] Reading order matches the visual/task order
- [ ] Status messages (success/error/progress) are announced without forcing focus unless needed

## Dynamic Type and Layout

- [ ] Text scales at the largest accessibility sizes
- [ ] Important information is not truncated/clipped
- [ ] Primary actions remain visible and usable
- [ ] Layout remains usable in portrait and landscape (when orientation support applies)

## Focus and Keyboard / Switch Control (if applicable)

- [ ] Focus order is logical for keyboard/switch navigation
- [ ] Focus is visible
- [ ] Focused element is not obscured by keyboard/sheet/sticky UI
- [ ] Focus is not trapped in custom controls or modals

## Color and Contrast

- [ ] Information is not conveyed by color alone
- [ ] Error/selected/disabled states are understandable without color
- [ ] Text contrast is sufficient for the feature's text styles
- [ ] Non-text contrast is sufficient for control boundaries, focus indicators, and states

## Touch Targets and Gestures

- [ ] Small controls meet target size/spacing expectations or have equivalent alternatives
- [ ] Gesture-driven actions have equivalent single-pointer controls when required
- [ ] Drag operations have non-drag alternatives when required

## Authentication and Forms (if applicable)

- [ ] Password/OTP fields allow paste where appropriate
- [ ] Password manager / AutoFill / one-time-code flows work
- [ ] Error messages are announced and understandable
- [ ] Previously entered information is reused or selectable in multi-step flows

## Final Check

- [ ] No new accessibility regressions were introduced by the proposed fixes
