# Codex Skill Updater

Automated sync of upstream skill sources into local Codex skills (`~/.codex/skills`), plus a repo snapshot of the current local skill set.

This repo is designed so a human or another AI can continue operations without reverse engineering the script.

## Goal

Keep locally installed Codex skills aligned with upstream Composio repos, while preserving predictable ownership and safe cleanup behavior.

## Scope

The updater currently manages skills from:

- `ComposioHQ/awesome-codex-skills` (`master`)
- `ComposioHQ/awesome-claude-skills` (`master`)
- `ComposioHQ/skills` (`main`)

It only manages directories containing `SKILL.md`.

This repo can also snapshot every locally installed skill into a checked-in `skills/` directory for backup, review, or publishing.

## Core Behavior

Each run performs these steps:

1. Downloads fresh zip snapshots of each source repo from GitHub.
3. Discovers all skill directories (`**/SKILL.md`) in source repos.
4. Excludes system/built-in skill names (to avoid collisions).
5. Resolves duplicate skill names with **first-repo-wins** precedence.
6. Syncs current managed skills into `~/.codex/skills/<skill-name>`.
7. Removes previously managed skills that are no longer present upstream.
8. Writes a manifest file of currently managed skills.

## Deterministic Rules

### Precedence Rule

When two repos contain the same skill folder name:

- Winner is whichever repo appears first in `repos` list in script.
- Current order:
  1. `awesome-codex-skills`
  2. `awesome-claude-skills`
  3. `skills` (`composio-skills-repo`)

### Managed vs Unmanaged

- Managed skills are tracked in:
  - `~/.codex/skills/.composio-managed-skills.txt`
- A skill is deleted only if:
  - It existed in previous manifest, and
  - It no longer exists in current discovered set.
- Skills never managed by this script are not deleted by manifest cleanup.

### System Skill Exclusion

System names are hardcoded in `update-composio-skills.sh` and skipped intentionally to avoid overriding built-in behavior.

## Files and Responsibilities

- `update-composio-skills.sh`
  - Single entrypoint.
  - Bash wrapper + embedded Python logic.
  - Source of truth for repo list, precedence, exclusions, and sync logic.
  - Uses GitHub zip snapshots instead of persistent local git clones.
- `sync-local-skills.sh`
  - Copies every locally installed skill from `~/.codex/skills` into this repo under `./skills/`.
  - Removes stale repo snapshots that no longer exist locally.
  - Writes `./skills-manifest.txt` as the canonical snapshot index.

## Runtime Paths

- Canonical script in this repo:
  - `./update-composio-skills.sh`
- Deployed cron-safe script path:
  - `~/.codex/bin/update-composio-skills.sh`
- Temporary repo snapshots:
  - Created under system temp dir via Python `TemporaryDirectory`
  - Deleted automatically after each successful or failed run
- Target skills directory:
  - `${CODEX_HOME:-~/.codex}/skills`
- Manifest:
  - `${CODEX_HOME:-~/.codex}/skills/.composio-managed-skills.txt`
- Repo snapshot destination:
  - `./skills/`
- Repo snapshot manifest:
  - `./skills-manifest.txt`

## Dependencies

Required:

- `bash`
- `python3`
- outbound HTTPS access to `github.com` / `codeload.github.com`

Optional:

- `rsync` (preferred for sync; falls back to delete+copy when unavailable)

## Usage

```bash
chmod +x update-composio-skills.sh
./update-composio-skills.sh
```

To deploy the script where cron can execute it reliably on macOS:

```bash
mkdir -p ~/.codex/bin
cp update-composio-skills.sh ~/.codex/bin/update-composio-skills.sh
chmod +x ~/.codex/bin/update-composio-skills.sh
```

To target a non-default Codex home:

```bash
CODEX_HOME=/path/to/codex-home ./update-composio-skills.sh
```

To sync the current local skill set into this repo:

```bash
./sync-local-skills.sh
```

## Expected Output

At minimum:

- `Managed skills: <count>`
- `Manifest: <path>`

When upstream removals happen:

- `Removed <skill-name>`

For repo snapshot runs:

- `Synced skills: <count>`
- `Manifest: <repo>/skills-manifest.txt`

## Scheduling (Cron)

Current weekly schedule example:

```bash
0 9 * * 1 /Users/kunanonjarat/.codex/bin/update-composio-skills.sh >> ~/.codex/skill-update.log 2>&1
```

Inspect cron entry:

```bash
crontab -l
```

Inspect updater logs:

```bash
tail -n 200 ~/.codex/skill-update.log
```

## Validation Checklist

After changing the updater:

1. Syntax check:
   - `bash -n update-composio-skills.sh`
2. Run once manually:
   - `./update-composio-skills.sh`
3. Confirm manifest exists and non-empty:
   - `wc -l ~/.codex/skills/.composio-managed-skills.txt`
4. Spot-check one synced skill:
   - `ls ~/.codex/skills | head`

After changing local snapshot behavior:

1. Run once manually:
   - `./sync-local-skills.sh`
2. Confirm manifest exists and count matches repo snapshot:
   - `wc -l skills-manifest.txt`
   - `find skills -mindepth 1 -maxdepth 1 -type d | wc -l`

## Troubleshooting

### GitHub auth failures

- This updater uses public GitHub archive downloads and does not require `gh`.
- If corporate proxy or network policy blocks GitHub archive downloads, test:
  - `curl -I https://codeload.github.com`

### Branch rename upstream

If a source branch changes (for example `master` -> `main`), update the `ref` field in `repos` list in `update-composio-skills.sh`.

### Permission errors in cron

- Confirm script is executable:
  - `chmod +x ~/.codex/bin/update-composio-skills.sh`
- Keep the cron-run script outside Desktop/Documents/Downloads to avoid macOS privacy restrictions on background processes.
- Confirm `CODEX_HOME` target is writable by cron user.

### Slow run time

- Install `rsync` if absent.
- Expect snapshot download time from three source repos on each run.

## Change Guide (For AI/Handoffs)

When extending behavior, keep these invariants:

1. Maintain manifest-based cleanup contract.
2. Keep sync idempotent (safe to run repeatedly).
3. Preserve deterministic duplicate resolution.
4. Avoid overriding built-in/system skills unless explicitly intended.
5. Keep runtime independent from Desktop-only paths so cron can run unattended.

Recommended modification order:

1. Update `repos` and/or `system_names` in script.
2. Run local validation checklist.
3. Commit script and README together.
4. Run one manual sync and include result in commit/PR notes.

## Suggested Future Improvements

- Add dry-run mode (`--dry-run`) to preview changes.
- Add summary JSON output for machine parsing.
- Add lock file to avoid overlapping cron runs.
- Add optional alerts on sync failures.
