#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
MANIFEST="$SKILLS_DIR/.composio-managed-skills.txt"

mkdir -p "$SKILLS_DIR"

SKILLS_DIR="$SKILLS_DIR" MANIFEST="$MANIFEST" python3 - <<'PY'
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None)


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "codex-skill-updater"})
    with urllib.request.urlopen(request) as response:
        return response.read()


def safe_extract(zip_file: zipfile.ZipFile, dest_dir: Path) -> None:
    dest_root = dest_dir.resolve()
    for info in zip_file.infolist():
        extracted_path = (dest_dir / info.filename).resolve()
        if extracted_path == dest_root or str(extracted_path).startswith(f"{dest_root}{os.sep}"):
            continue
        raise RuntimeError("Archive contains files outside destination.")
    zip_file.extractall(dest_dir)


def prepare_repo_snapshot(repo: dict[str, str], work_dir: Path) -> Path:
    archive_dir = work_dir / repo["name"]
    archive_dir.mkdir(parents=True, exist_ok=True)
    zip_path = archive_dir / "repo.zip"
    zip_url = f"https://codeload.github.com/{repo['owner']}/{repo['repo']}/zip/{repo['ref']}"
    zip_path.write_bytes(download(zip_url))
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        safe_extract(zip_file, archive_dir)
        top_levels = {name.split("/")[0] for name in zip_file.namelist() if name}
    if not top_levels:
        raise RuntimeError("Downloaded archive was empty.")
    if len(top_levels) != 1:
        raise RuntimeError("Unexpected archive layout.")
    return archive_dir / next(iter(top_levels))


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
        "owner": "ComposioHQ",
        "repo": "awesome-codex-skills",
        "ref": "master",
    },
    {
        "name": "awesome-claude-skills",
        "owner": "ComposioHQ",
        "repo": "awesome-claude-skills",
        "ref": "master",
    },
    {
        "name": "skills",
        "owner": "ComposioHQ",
        "repo": "skills",
        "ref": "main",
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

skills_dir = Path(os.environ["SKILLS_DIR"])
manifest = Path(os.environ["MANIFEST"])

with tempfile.TemporaryDirectory(prefix="codex-skill-sync-") as tmp_root:
    repo_roots: dict[str, Path] = {}
    for repo in repos:
        repo_roots[repo["name"]] = prepare_repo_snapshot(repo, Path(tmp_root))

    # First-repo-wins ownership for duplicate skill names.
    owned: dict[str, tuple[Path, Path]] = {}
    for repo in repos:
        repo_path = repo_roots[repo["name"]]
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
