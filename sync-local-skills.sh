#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SOURCE_DIR="$CODEX_HOME/skills"
DEST_DIR="$REPO_DIR/skills"
MANIFEST="$REPO_DIR/skills-manifest.txt"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source skills directory not found: $SOURCE_DIR" >&2
  exit 1
fi

SOURCE_DIR="$SOURCE_DIR" DEST_DIR="$DEST_DIR" MANIFEST="$MANIFEST" python3 - <<'PY'
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def sync_dir(src: Path, dest: Path) -> None:
    if shutil.which("rsync"):
        dest.mkdir(parents=True, exist_ok=True)
        run(["rsync", "-a", "--delete", f"{src}/", f"{dest}/"])
        return

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


source_dir = Path(os.environ["SOURCE_DIR"]).expanduser()
dest_dir = Path(os.environ["DEST_DIR"]).resolve()
manifest = Path(os.environ["MANIFEST"]).resolve()

dest_dir.mkdir(parents=True, exist_ok=True)

source_skills = sorted(
    path for path in source_dir.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
)
source_names = [path.name for path in source_skills]
source_name_set = set(source_names)

for existing_dir in sorted(path for path in dest_dir.iterdir() if path.is_dir()):
    if existing_dir.name not in source_name_set:
        shutil.rmtree(existing_dir)
        print(f"Removed {existing_dir.name}")

synced = 0
for skill_dir in source_skills:
    sync_dir(skill_dir, dest_dir / skill_dir.name)
    synced += 1

manifest.write_text("".join(f"{name}\n" for name in source_names))

print(f"Synced skills: {synced}")
print(f"Manifest: {manifest}")
PY
