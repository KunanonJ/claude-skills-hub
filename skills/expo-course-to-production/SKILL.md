---
name: expo-course-to-production
description: Use when learning Expo or React Native from Expo Learn, Expo tutorials, courses, YouTube resources, or official Expo docs and converting that learning into a production-ready mobile app plan. Also use when choosing between Expo Go, development builds, Expo Router, EAS Build, EAS Update, app store submission, or when turning course lessons into issues, PRs, tests, and release workflows.
---

# Expo Course To Production

## Overview

Turn Expo learning material into executable product work. This skill bridges course content, official Expo docs, and the installed Expo plugin skills so Codex can move from "learn this" to repo-specific implementation without losing production discipline.

Source basis: Expo Learn, the Expo tutorial, Expo Router docs, development builds docs, EAS Build/Update docs, and the official Expo Skills for AI agents.

## Default Workflow

1. Identify the user's state:
   - No app yet: start with Expo tutorial concepts and project creation.
   - Existing Expo app: inspect SDK, router, app config, EAS config, tests, and package manager before advising.
   - Existing React Native app: evaluate whether Expo CLI, Expo Router, or EAS can be adopted incrementally.
   - Web-to-mobile app: map routes, state, auth, data, notifications, and platform-specific UX before writing code.
   - Release-stage app: focus on EAS Build, EAS Submit, EAS Update, credentials, CI, and rollback.

2. Select the course lane:
   - Beginner universal app: Expo tutorial, Expo Router basics, UI primitives, image/media, gestures, screenshots, platform differences, splash/icon/status bar.
   - Navigation and app architecture: Expo Router, typed routes, deep links, layout routes, native tabs, static web output.
   - Production development: Expo Go versus development builds, native libraries, config plugins, dev-client distribution.
   - Backend/data: API routes, data fetching, caching, offline behavior, auth/database integration.
   - Release and operations: EAS Build, internal distribution, store submission, updates, web deploys, CI/CD workflows.
   - Advanced native UI: SwiftUI, Jetpack Compose, Expo Modules API, DOM components for incremental web reuse.

3. Convert learning into work:
   - Produce a short project-specific learning map, not a generic course summary.
   - Break the next work into small issues or PR-sized slices.
   - Attach a verification command to each slice, such as `npx expo doctor`, `npm test`, `npx expo start --web`, simulator smoke tests, or EAS dry-run/config checks.
   - Keep implementation TDD-first when editing a repo: write the failing behavior test before production changes.
   - Defer secrets, store credentials, signing assets, and deployment credentials to `.env.example`, EAS secrets, CI secrets, or platform credential stores.

4. Route to implementation skills:
   - Use official Expo `building-native-ui` for screens, layouts, animations, and Expo Router UI work.
   - Use official Expo `native-data-fetching` for API calls, loaders, caching, offline handling, and data errors.
   - Use official Expo `expo-dev-client` when native modules, app icon/name/splash testing, or production-grade local development are needed.
   - Use official Expo `expo-deployment` for TestFlight, Google Play, App Store, EAS Hosting, and submissions.
   - Use official Expo `expo-cicd-workflows` for `.eas/workflows/` and build automation.
   - Use official Expo `upgrading-expo` before SDK upgrades or dependency repair.
   - Use local `react-native-expert` for general React Native component, platform, performance, keyboard, and list work.
   - Use local `advanced-automation-architect` before creating scheduled release, CI, or update automation.

## Course Output Templates

### Learning To Issues

```text
GOAL:
PROJECT STATE:
EXPO SDK / ROUTER STATE:
COURSE LANE:
OFFICIAL EXPO SKILL TO USE NEXT:
ISSUES:
1. Title:
   Behavior:
   Test first:
   Implementation notes:
   Verification:
2. Title:
   Behavior:
   Test first:
   Implementation notes:
   Verification:
RISKS / CREDENTIALS:
NEXT COMMAND:
```

### App Blueprint

```text
APP OBJECTIVE:
TARGET PLATFORMS:
ROUTING MODEL:
DATA / AUTH:
NATIVE CAPABILITIES:
BUILD MODE:
RELEASE PATH:
COURSE MODULES TO APPLY:
MILESTONE 1:
MILESTONE 2:
MILESTONE 3:
VERIFICATION PLAN:
ROLLBACK PLAN:
```

## Guardrails

- Prefer current project evidence over generic Expo advice. Inspect `package.json`, `app.json`, `app.config.*`, `app/`, `eas.json`, lockfiles, and existing tests first.
- Do not assume the latest Expo SDK matches the app. Read the installed `expo` package and use version-matched docs when available.
- Start with Expo Go only for compatible learning/prototype work. Move to a development build as soon as native libraries, app config changes, or production-grade testing require it.
- Do not run EAS Build, EAS Submit, publish updates, or change signing credentials without explicit user approval.
- Do not hardcode API keys, EAS tokens, Apple credentials, Google service account files, or release secrets.
- Keep course-derived tasks small enough for independent PRs and rerunnable verification.

## References

- `references/course-map.md`: Expo Learn and official docs mapped to skill routes, project stages, and verification commands.
