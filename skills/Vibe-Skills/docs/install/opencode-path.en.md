# OpenCode Install and Use Guide

## Why This Guide Exists

- the generic install prompts can already install `opencode`
- this guide does not replace the generic install prompts; it expands OpenCode-specific details
- it is split out because OpenCode also needs clearer coverage of direct install/check, its default target root, project-local isolation, the files written by install, and host-local boundaries, which would make the common install docs too heavy

## What The Repository Installs

- repo-distributed content
- Vibe-Skills skill content
- `.vibeskills/host-settings.json`
- `.vibeskills/host-closure.json`
- `.vibeskills/bin/*-specialist-wrapper.*`
- an `opencode.json.example` scaffold

## What Still Stays Host-Local

- the real `~/.config/opencode/opencode.json`
- provider credentials
- plugin installation
- MCP trust decisions

## Global Install

Shell:

```bash
./install.sh --host opencode
./check.sh --host opencode
```

PowerShell:

```powershell
pwsh -NoProfile -File ./install.ps1 -HostId opencode
pwsh -NoProfile -File ./check.ps1 -HostId opencode
```

Default target root:

- `OPENCODE_HOME` when set
- otherwise the real host root `~/.config/opencode`

This default target root is the real host config directory `~/.config/opencode`.

The default examples omit `--profile`, which is equivalent to `full`.
If you need the “Framework Only + Customizable Governance” variant, append `--profile minimal` to install/check explicitly.

## Project-Local Install

Use a project-local OpenCode root when you want the install result to stay inside the repo:

```bash
./install.sh --host opencode --target-root ./.opencode
./check.sh --host opencode --target-root ./.opencode
```

The same target can be used from PowerShell with `-TargetRoot .\.opencode`.
For the framework-only variant, also append `-Profile minimal` explicitly.

## What Gets Written

The install writes:

- `skills/**`
- `.vibeskills/host-settings.json`
- `.vibeskills/host-closure.json`
- `.vibeskills/install-ledger.json`
- `.vibeskills/bin/*-specialist-wrapper.*`
- `opencode.json.example`

The install does not create a new real `opencode.json`, and it does not take ownership of that file.
If you need to change native OpenCode settings, keep doing that on the host side.

## How To Use

After install, the intended entry surfaces are:

- `/vibe`
- `/vibe-implement`
- `/vibe-review`

You can also invoke the skill directly in chat, for example:

- `Use the vibe skill to plan this change.`
- `Use the vibe skill to implement the approved plan.`

These entrypoints stay skill-native. When Vibe is not explicitly invoked, the sidecar state remains silent and does not try to take over native OpenCode configuration.

Custom agents installed by this path:

- `vibe-plan`
- `vibe-implement`
- `vibe-review`

## Verification

Use the shared repo health check first:

```bash
./check.sh --host opencode
```

The repository also ships a smoke verifier:

```bash
python3 ./scripts/verify/runtime_neutral/opencode_preview_smoke.py --repo-root . --write-artifacts
```

## Current Verification Note

The committed smoke verifier has been validated on local OpenCode CLI `1.2.27` and confirms that:

- `opencode debug paths` resolves the isolated OpenCode root correctly
- `opencode debug config` still parses successfully after install
- `opencode debug skill --pure` detects the installed `vibe` skill
- `opencode debug agent vibe-plan` detects the installed agent

Additional note:

- `opencode debug skill` can emit a truncated oversized skill dump when many skills are installed, so it is currently kept as a telemetry/warning surface instead of a hard startup-recovery gate
- startup recovery is judged primarily through `debug config` and `debug agent`, because those directly validate config parsing and agent loading

If you need the deeper adapter contract and proof details, continue with `dist/*`, `adapters/*`, and `docs/universalization/*`.
