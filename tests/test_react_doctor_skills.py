from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_react_doctor_source_is_registered() -> None:
    sync_script = ROOT / "sync-listed-sources.sh"

    assert '{"kind": "repo", "repo": "millionco/react-doctor"}' in (
        sync_script.read_text()
    )


def test_react_doctor_skills_are_installed_and_traceable() -> None:
    expected_skills = {
        "react-doctor": ".agents/skills/react-doctor",
        "rule-research": ".agents/skills/rule-research",
        "rule-validate": ".agents/skills/rule-validate",
        "rule-writing": ".agents/skills/rule-writing",
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
        assert row["repo_spec"] == "millionco/react-doctor"
        assert row["relative_path"] == upstream_path
        assert row["discovered_from"] == "https://github.com/millionco/react-doctor"


def test_react_doctor_skill_keeps_canonical_command_and_playbook() -> None:
    skill_text = (ROOT / "skills" / "react-doctor" / "SKILL.md").read_text()

    assert "npx react-doctor@latest --verbose --diff" in skill_text
    assert "https://www.react.doctor/prompts/react-doctor-agent.md" in skill_text
