from __future__ import annotations

import csv
from pathlib import Path

from app.skill_quality import KEEP_SKILLS


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_is_exactly_the_lean_keep_list() -> None:
    manifest = [
        line.strip()
        for line in (ROOT / "skills-manifest.txt").read_text().splitlines()
        if line.strip()
    ]

    assert len(manifest) == 100
    assert manifest == sorted(manifest)
    assert set(manifest) == KEEP_SKILLS


def test_each_manifest_skill_has_resolvable_skill_file() -> None:
    manifest = [
        line.strip()
        for line in (ROOT / "skills-manifest.txt").read_text().splitlines()
        if line.strip()
    ]

    for skill_name in manifest:
        assert (ROOT / "skills" / skill_name / "SKILL.md").is_file()


def test_no_extra_top_level_skill_directories() -> None:
    top_level_dirs = {
        path.name for path in (ROOT / "skills").iterdir() if path.is_dir()
    }

    assert top_level_dirs == KEEP_SKILLS


def test_no_top_level_skill_files() -> None:
    top_level_files = [
        path.name for path in (ROOT / "skills").iterdir() if path.is_file()
    ]

    assert top_level_files == []


def test_source_map_matches_manifest() -> None:
    manifest = [
        line.strip()
        for line in (ROOT / "skills-manifest.txt").read_text().splitlines()
        if line.strip()
    ]
    with (ROOT / "skills-source-map.tsv").open(newline="") as source_map_file:
        rows = list(csv.DictReader(source_map_file, delimiter="\t"))

    assert len(rows) == 100
    assert [row["skill_name"] for row in rows] == manifest
    for row in rows:
        assert row["repo_spec"]
        assert row["relative_path"]
        assert row["discovered_from"]


def test_no_broken_symlinks_under_skills() -> None:
    broken = [
        path
        for path in (ROOT / "skills").rglob("*")
        if path.is_symlink() and not path.exists()
    ]

    assert broken == []
