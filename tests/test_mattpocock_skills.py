from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mattpocock_skills_source_is_registered() -> None:
    sync_script = ROOT / "sync-listed-sources.sh"

    assert '{"kind": "repo", "repo": "mattpocock/skills"}' in sync_script.read_text()


def test_mattpocock_skills_are_installed_and_traceable() -> None:
    expected_skills = {
        "diagnose": "skills/engineering/diagnose",
        "grill-with-docs": "skills/engineering/grill-with-docs",
        "setup-matt-pocock-skills": "skills/engineering/setup-matt-pocock-skills",
        "tdd": "skills/engineering/tdd",
    }

    manifest_names = {
        line.strip()
        for line in (ROOT / "skills-manifest.txt").read_text().splitlines()
        if line.strip()
    }

    with (ROOT / "skills-source-map.tsv").open(newline="") as source_map_file:
        rows = list(csv.DictReader(source_map_file, delimiter="\t"))

    rows_by_name = {row["skill_name"]: row for row in rows}

    for skill_name, upstream_path in expected_skills.items():
        assert skill_name in manifest_names
        assert (ROOT / "skills" / skill_name / "SKILL.md").is_file()

        row = rows_by_name[skill_name]
        assert row["repo_spec"] == "mattpocock/skills"
        assert row["relative_path"] == upstream_path
        assert row["discovered_from"] == "https://github.com/mattpocock/skills"
