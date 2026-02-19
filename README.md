# Codex Skill Updater

Automated sync of Composio skill repositories into local Codex skills (`~/.codex/skills`).

This repo is designed so a human or another AI can continue operations without reverse engineering the script.

## Goal

Keep locally installed Codex skills aligned with upstream Composio repos, while preserving predictable ownership and safe cleanup behavior.

## Scope

The updater currently manages skills from:

- `ComposioHQ/awesome-codex-skills` (`master`)
- `ComposioHQ/awesome-claude-skills` (`master`)
- `ComposioHQ/skills` (`main`)

It only manages directories containing `SKILL.md`.

## Core Behavior

Each run performs these steps:

1. Ensures each source repo exists locally (clone if missing).
2. Fast-forwards each local repo to latest upstream branch.
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

## Runtime Paths

- Script path (this repo): `./update-composio-skills.sh`
- Local source clones:
  - `../awesome-codex-skills`
  - `../awesome-claude-skills`
  - `../composio-skills-repo`
- Target skills directory:
  - `${CODEX_HOME:-~/.codex}/skills`
- Manifest:
  - `${CODEX_HOME:-~/.codex}/skills/.composio-managed-skills.txt`

## Dependencies

Required:

- `bash`
- `python3`
- `git`

Optional:

- `rsync` (preferred for sync; falls back to delete+copy when unavailable)

## Usage

```bash
chmod +x update-composio-skills.sh
./update-composio-skills.sh
```

To target a non-default Codex home:

```bash
CODEX_HOME=/path/to/codex-home ./update-composio-skills.sh
```

## Expected Output

At minimum:

- `Managed skills: <count>`
- `Manifest: <path>`

When upstream removals happen:

- `Removed <skill-name>`

## Scheduling (Cron)

Current weekly schedule example:

```bash
0 9 * * 1 /Users/kunanonjarat/Desktop/Skills/update-composio-skills.sh >> ~/.codex/skill-update.log 2>&1
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

## Troubleshooting

### GitHub auth failures

- Ensure `git` can pull over configured protocol (HTTPS/SSH).
- Re-authenticate if required:
  - `gh auth login -h github.com`

### Branch rename upstream

If a source branch changes (for example `master` -> `main`), update the `branch` field in `repos` list in `update-composio-skills.sh`.

### Permission errors in cron

- Confirm script is executable:
  - `chmod +x /Users/kunanonjarat/Desktop/Skills/update-composio-skills.sh`
- Confirm `CODEX_HOME` target is writable by cron user.

### Slow run time

- Install `rsync` if absent.
- Keep local clone dirs on local disk (not remote mount).

## Change Guide (For AI/Handoffs)

When extending behavior, keep these invariants:

1. Maintain manifest-based cleanup contract.
2. Keep sync idempotent (safe to run repeatedly).
3. Preserve deterministic duplicate resolution.
4. Avoid overriding built-in/system skills unless explicitly intended.

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
