---
name: jahro-snapshots
description: >
  Guides snapshot mode selection, capture workflows, QA sharing, and
  team setup for Jahro Snapshots. Use when the user mentions snapshots,
  bug capture, sharing logs, streaming, recording, QA workflow, team
  collaboration, or wants to share debugging sessions with their team.
---

# Jahro Snapshots

Help users capture, share, and collaborate on debugging sessions using Jahro's snapshot system.

## What Snapshots Capture

Each snapshot session bundles:
- **Logs**: all `Debug.Log`, `Debug.LogWarning`, `Debug.LogError` output with stack traces
- **Screenshots**: captured during the session with timestamp correlation
- **Device metadata**: platform, OS version, Unity version, device specs
- **Team member**: who captured the session

Sessions appear in-game with status indicators and can be uploaded or streamed to the Jahro web console for team access via shareable URLs.

## Snapshot Modes

Configure in **Tools → Jahro Settings → Snapshots Settings**.

| Mode | Behavior | Best For |
|:-----|:---------|:---------|
| **Recording** | Stores locally until manual upload | Offline development, privacy-sensitive environments, controlled uploads |
| **Streaming — All** | Auto-streams logs/screenshots live (~5s intervals) to cloud | Real-time team collaboration, full team visibility |
| **Streaming — Except Editor** | Streams on devices, records locally in Editor | Hybrid: QA devices stream, developers keep Editor sessions private |

### Mode selection guide

| Situation | Recommended Mode |
|:----------|:----------------|
| Solo developer, mostly in Editor | Recording |
| QA team testing on mobile devices | Streaming — All or Streaming — Except Editor |
| Full team wants real-time updates | Streaming — All |
| Privacy-sensitive project | Recording |
| Intermittent network connectivity | Recording (upload when connected) |
| QA on devices + dev in Editor | Streaming — Except Editor |

## QA Capture Workflow

Step-by-step for QA testers on mobile:

1. **Open console**: Triple-tap at top of screen (or tap the Launch Button)
2. **Switch to Snapshots tab**
3. **Tap "Start Snapshot"**: session begins capturing logs and screenshots
4. **Reproduce the issue**: play normally while Jahro records everything
5. **Take screenshots**: tap the screenshot button at key moments
6. **Tap "Stop Snapshot"**: session ends
7. **Share**:
   - **Recording mode**: Tap "Upload" → wait for upload → copy URL
   - **Streaming mode**: URL is already available → copy URL
8. **Share the URL** via Slack, email, or bug tracker

The developer opens the URL in a browser and sees the full session in the Jahro web console — logs (filterable), screenshots (lightbox viewer), and device metadata.

## Session Management

### Session statuses

| Status | Meaning | Next Action |
|:-------|:--------|:------------|
| Recording | Actively collecting logs/screenshots | Stop when done |
| Recorded | Stopped, stored locally | Upload to share |
| Uploading | Upload in progress | Wait for completion |
| Uploaded | Successfully uploaded | Copy URL to share |
| Streaming | Live-streaming to cloud | Stop when done |
| Streamed | Streaming complete and flushed | Copy URL to share |

If an error occurs (network failure, auth issue), an inline error message appears with a **Retry** button.

### Local storage

- 10 most recent snapshots kept locally with automatic rotation
- Older sessions are automatically cleaned up
- Editable titles (up to 100 characters) — tap the pencil icon to rename

### Streaming behavior

When streaming:
- Data sent in chunks approximately every **5 seconds**
- Duplicate logs within the same chunk are collapsed (auto-deduplication)
- Near real-time updates on the web console
- If network drops, buffered data is sent when connection resumes

## Web Console (Light Touch)

After upload/stream, sessions are viewable at **console.jahro.io**:

- **Logs Viewer**: Filter by Debug/Warning/Error/Commands, full-text search, stack traces
- **Screenshots Gallery**: Lightbox viewer with zoom, timestamp correlation to logs
- **Device Metadata**: Platform, OS, Unity version, device specs, team member
- **Shareable Links**: Generate URLs that open directly in the web console

The web console is outside the scope of this skill — for team management details, refer to Jahro's web documentation.

## Team Setup

### API key configuration

Each Unity project needs an API key to enable snapshot uploads:

1. Create team at **console.jahro.io**
2. Create a project under the team
3. Go to **Project → API Keys** → copy key
4. In Unity → **Tools → Jahro Settings → Account** → paste key
5. Key validates automatically, shows project/team info

One API key per project. All team members building from the same Unity project share the same key (via the `jahro-settings.asset` file in version control).

### Role-based access

| Role | Can Do |
|:-----|:-------|
| **Owner** | Everything: billing, team settings, roles, transfers |
| **Admin** | Manage members, configure integrations, access all content |
| **Member** | Create/view/edit snapshots, logs, screenshots |

### Team workflow recommendations

- Include `Assets/Jahro/Resources/jahro-settings.asset` in version control
- Use **Streaming — Except Editor** so QA devices stream automatically while developers control their own sessions
- Establish naming conventions for snapshot titles (e.g., "BUG-123: Crash on level 5")
- QA should paste snapshot URLs directly into bug tickets

## Contextual Awareness

| Pattern | Suggestion |
|:--------|:-----------|
| User mentions QA, testers, or bug reports | Guide snapshot setup for QA workflow |
| User mentions sharing logs or screenshots | Explain snapshot sharing flow |
| User mentions mobile debugging | Highlight triple-tap + streaming for cable-free debugging |
| User asks about Recording vs Streaming | Walk through mode selection guide |
| API key not configured | Guide API key setup before snapshot features work |

## Verification

After configuring snapshots:

> **Verify:** Enter Play Mode → open Jahro console → Snapshots tab → Start a snapshot → play for a few seconds → Stop → Upload (or check stream URL). Open the URL in a browser to confirm logs and screenshots appear in the web console.

If snapshots fail, suggest the jahro-troubleshooting skill — common causes: missing API key, network issues, wrong snapshot mode for the platform.
