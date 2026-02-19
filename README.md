# Codex Skill Updater

Sync Composio skills into your local Codex skills directory.

## What It Does

- Pulls latest changes from:
  - `ComposioHQ/awesome-codex-skills` (`master`)
  - `ComposioHQ/awesome-claude-skills` (`master`)
  - `ComposioHQ/skills` (`main`)
- Updates managed skills under `~/.codex/skills`
- Tracks managed skills in `~/.codex/skills/.composio-managed-skills.txt`
- Removes previously managed skills that no longer exist upstream

## Files

- `update-composio-skills.sh`: sync script

## Usage

```bash
chmod +x update-composio-skills.sh
./update-composio-skills.sh
```

## Weekly Schedule (cron)

```bash
0 9 * * 1 /Users/kunanonjarat/Desktop/Skills/update-composio-skills.sh >> ~/.codex/skill-update.log 2>&1
```
