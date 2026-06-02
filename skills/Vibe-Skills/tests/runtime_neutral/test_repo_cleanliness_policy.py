from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _gitignore_patterns() -> set[str]:
    lines = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    return {
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_vibeskills_local_state_is_ignored_and_classified() -> None:
    policy = json.loads(
        (REPO_ROOT / "config" / "repo-cleanliness-policy.json").read_text(encoding="utf-8")
    )

    assert ".vibeskills/" in _gitignore_patterns()
    assert ".vibeskills/" in policy["shared_repo_ignores"]
    assert ".vibeskills/" in policy["local_noise_paths"]
