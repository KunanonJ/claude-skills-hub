#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
MANIFEST="$SKILLS_DIR/.composio-managed-skills.txt"

mkdir -p "$SKILLS_DIR"

BASE_DIR="$BASE_DIR" SKILLS_DIR="$SKILLS_DIR" MANIFEST="$MANIFEST" python3 - <<'PY'
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None)


def ensure_repo(path: Path, url: str, branch: str) -> None:
    if not (path / ".git").exists():
        run(["git", "clone", "--single-branch", "--branch", branch, url, str(path)])
    run(["git", "-C", str(path), "fetch", "origin", branch, "--quiet"])
    run(["git", "-C", str(path), "checkout", branch, "--quiet"])
    run(["git", "-C", str(path), "merge", "--ff-only", f"origin/{branch}", "--quiet"])


def list_skill_dirs(repo_path: Path) -> list[Path]:
    return sorted(p.parent.relative_to(repo_path) for p in repo_path.rglob("SKILL.md"))


def sync_dir(src: Path, dest: Path) -> None:
    if shutil.which("rsync"):
        dest.mkdir(parents=True, exist_ok=True)
        run(["rsync", "-a", "--delete", f"{src}/", f"{dest}/"])
        return

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


repos: list[dict[str, str]] = [
    {
        "name": "awesome-codex-skills",
        "path": os.path.join(os.environ["BASE_DIR"], "awesome-codex-skills"),
        "url": "https://github.com/ComposioHQ/awesome-codex-skills.git",
        "branch": "master",
    },
    {
        "name": "awesome-claude-skills",
        "path": os.path.join(os.environ["BASE_DIR"], "awesome-claude-skills"),
        "url": "https://github.com/ComposioHQ/awesome-claude-skills.git",
        "branch": "master",
    },
    {
        "name": "skills",
        "path": os.path.join(os.environ["BASE_DIR"], "composio-skills-repo"),
        "url": "https://github.com/ComposioHQ/skills.git",
        "branch": "main",
    },
]

system_names = {
    "atlas",
    "cloudflare-deploy",
    "doc",
    "figma",
    "figma-implement-design",
    "gh-address-comments",
    "gh-fix-ci",
    "imagegen",
    "jupyter-notebook",
    "linear",
    "notion-knowledge-capture",
    "notion-meeting-intelligence",
    "notion-research-documentation",
    "notion-spec-to-implementation",
    "openai-docs",
    "pdf",
    "playwright",
    "screenshot",
    "security-best-practices",
    "security-ownership-map",
    "security-threat-model",
    "skill-creator",
    "skill-installer",
    "sora",
    "speech",
    "spreadsheet",
    "transcribe",
    "yeet",
}

base_dir = Path(os.environ["BASE_DIR"])
skills_dir = Path(os.environ["SKILLS_DIR"])
manifest = Path(os.environ["MANIFEST"])

for repo in repos:
    ensure_repo(Path(repo["path"]), repo["url"], repo["branch"])

# First-repo-wins ownership for duplicate skill names.
owned: dict[str, tuple[Path, Path]] = {}
for repo in repos:
    repo_path = Path(repo["path"])
    for rel_skill_dir in list_skill_dirs(repo_path):
        skill_name = rel_skill_dir.name
        if skill_name in system_names:
            continue
        if skill_name not in owned:
            owned[skill_name] = (repo_path, rel_skill_dir)

previous_managed: set[str] = set()
if manifest.exists():
    previous_managed = {line.strip() for line in manifest.read_text().splitlines() if line.strip()}

current_managed = set(owned.keys())

# Remove skills no longer managed by these repos.
for removed_name in sorted(previous_managed - current_managed):
    target = skills_dir / removed_name
    if target.exists():
        shutil.rmtree(target)
        print(f"Removed {removed_name}")

updated = 0
for skill_name in sorted(current_managed):
    repo_path, rel_skill_dir = owned[skill_name]
    src = repo_path / rel_skill_dir
    dest = skills_dir / skill_name
    sync_dir(src, dest)
    updated += 1

manifest.write_text("".join(f"{name}\n" for name in sorted(current_managed)))

print(f"Managed skills: {updated}")
print(f"Manifest: {manifest}")
PY
