---
name: github-codespaces-dev
description: "Configure GitHub Codespaces for a repo — devcontainer.json, prebuilds, dotfiles, port forwarding, and machine type selection. Trigger when the user mentions Codespaces, devcontainer, cloud dev environment, '.devcontainer', codespace prebuild, or asks to set up a reproducible dev environment in the cloud. Sourced from github.com/skills/code-with-codespaces."
---

# GitHub Codespaces Dev Environment

Set up reproducible cloud development environments in Codespaces. The goal: any contributor can hit "Open in Codespace" and be productive in under 60 seconds with the right tools, extensions, and ports already configured.

## When to Use

- Onboarding pain — new contributors take hours/days to get a working dev env.
- "Works on my machine" — local dev environments drift.
- Browser-based dev — Chromebooks, iPads, locked-down laptops.
- Demo environments — share a working setup via URL.
- Heavy compute — train models, run integration tests on bigger VMs than local.

## The Devcontainer File

Everything starts at `.devcontainer/devcontainer.json` in repo root. This file is the contract.

### Minimal example

```json
{
  "name": "Node.js 20",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "forwardPorts": [3000],
  "postCreateCommand": "npm ci",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  }
}
```

### Full-featured example

```json
{
  "name": "Full Stack TS + Postgres",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/node:1": { "version": "20" }
  },
  "forwardPorts": [3000, 5432],
  "portsAttributes": {
    "3000": { "label": "App", "onAutoForward": "openBrowser" },
    "5432": { "label": "Postgres", "onAutoForward": "silent" }
  },
  "postCreateCommand": "npm ci && npm run db:migrate",
  "postStartCommand": "npm run dev &",
  "hostRequirements": { "cpus": 4, "memory": "8gb", "storage": "32gb" },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        "Prisma.prisma"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  },
  "remoteUser": "node"
}
```

## Key Fields

| Field | What it does | When you need it |
|---|---|---|
| `image` | Base container image | Always |
| `features` | Composable add-ons (Docker, gh CLI, languages) | Most cases |
| `forwardPorts` | Auto-forward these container ports | When app listens on a port |
| `postCreateCommand` | Runs once when container is built | Install deps, run migrations |
| `postStartCommand` | Runs every time codespace starts | Start background services |
| `hostRequirements` | Min VM size — forces Codespaces to pick a bigger machine | Heavy builds, model training |
| `customizations.vscode.extensions` | Pre-install extensions | Always — saves manual setup |
| `remoteUser` | Run as non-root | Production-parity dev |

## Prebuilds — Cut Cold Start to Seconds

Without prebuilds, every codespace builds the container from scratch (5–15 min). Prebuilds run on a schedule + on push to keep an image warm.

Enable at **Settings → Codespaces → Prebuild configurations → Set up prebuild**:
- Pick repo + branch (usually `main`)
- Pick regions (the ones your team uses)
- Trigger: every push, daily, or on devcontainer changes
- Storage cost: ~$0.07/GB/month per region

Verified prebuild status shows on the "Create codespace" screen with a green checkmark.

## Port Forwarding Gotchas

- **Auto-forwarded** ports are private by default. Click in the Ports panel to make a port public if sharing a demo URL.
- **Privacy levels**: `private` → only you can access; `org` → anyone in the org with the URL; `public` → anyone with the URL.
- Never make ports with unauthenticated admin panels public. Codespaces URLs are guessable enough.

## Dotfiles — Personal Customization

Configure per-user dotfiles at **Settings → Codespaces → Dotfiles repository**. Codespaces will clone that repo into every codespace you create and run `install.sh` / `bootstrap.sh` / etc. Good for:

- Shell config (`.zshrc`, `.bashrc`)
- Git config (`git config --global user.signingkey ...`)
- Personal aliases, custom prompts

Don't put repo-specific tooling here. That belongs in `devcontainer.json` so teammates get it too.

## Common Patterns

### Docker-in-Docker for local containers

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "moby": true,
      "dockerDashComposeVersion": "v2"
    }
  }
}
```

Lets `docker compose up` work inside the codespace.

### Postgres sidecar via docker-compose

`.devcontainer/docker-compose.yml`:
```yaml
services:
  app:
    image: mcr.microsoft.com/devcontainers/typescript-node:20
    volumes: ["..:/workspace:cached"]
    command: sleep infinity
    network_mode: service:db
  db:
    image: postgres:16
    environment: { POSTGRES_PASSWORD: postgres }
    volumes: ["postgres-data:/var/lib/postgresql/data"]
volumes: { postgres-data: }
```

`.devcontainer/devcontainer.json`:
```json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [3000, 5432]
}
```

### Secrets

Add at **Settings → Codespaces → Secrets**. Available as env vars in every codespace for that repo. Scope to specific repos to avoid leaking team-wide.

```json
{
  "containerEnv": {
    "DATABASE_URL": "${localEnv:DATABASE_URL}"
  }
}
```

## Anti-Patterns

- ❌ Committing `.env` to the repo so codespaces "just work" — use Codespaces Secrets.
- ❌ `postCreateCommand` with a 10-minute install — use prebuilds instead.
- ❌ Custom base images you maintain yourself — start from `mcr.microsoft.com/devcontainers/*` and add features.
- ❌ Hardcoding `forwardPorts` for ports the app doesn't actually use — wastes UI noise.
- ❌ Running as root — set `remoteUser` to a non-root user.
- ❌ Setting `hostRequirements.cpus: 32` because "more is better" — costs $0.36/hr+, not always available.

## Quick Setup Checklist

- [ ] `.devcontainer/devcontainer.json` exists in repo root
- [ ] `image` points to a maintained devcontainers image
- [ ] `postCreateCommand` installs deps idempotently
- [ ] VS Code extensions list matches project tooling (ESLint, Prettier, language servers)
- [ ] `forwardPorts` covers every port the app listens on
- [ ] Repo secrets configured for any required env vars
- [ ] Prebuild enabled on `main` for the team's primary region
- [ ] README has a "Open in Codespace" badge linking to `https://codespaces.new/<owner>/<repo>`

## References

- Source course: https://github.com/skills/code-with-codespaces
- Devcontainer spec: https://containers.dev/implementors/json_reference/
- Prebuilds: https://docs.github.com/en/codespaces/prebuilding-your-codespaces
- Features index: https://containers.dev/features
