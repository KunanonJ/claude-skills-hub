# Verification-Core Retired Field Hard Erasure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove all current verification-core reads and outputs derived from the retired `route_authority_candidates` and `stage_assistant_candidates` fields.

**Architecture:** Escalate the terminology gate first so the current verification-core residue becomes blocking, then clean each audit module with current-only behavior tests. The implementation keeps old fixture fields readable as ignored input, but audit rows, scoring, role decisions, CSV, JSON, and Markdown are based only on current fields such as `skill_candidates` and `defaults_by_task`.

**Tech Stack:** Python 3, pytest/unittest runtime-neutral tests, verification-core audit modules, JSON terminology policy, PowerShell verification gates, ripgrep.

---

## File Structure

**Terminology gate**

- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
  - Owns the JSON contract for `vibe-routing-terminology-hard-cleanup-scan.ps1`; it must require zero `review` hits after this cleanup.
- Modify: `config/routing-terminology-hard-cleanup.json`
  - Owns the current-surface terminology budget; remove the four verification-core audit modules from `compatibility_review_files`.

**Verification-core modules**

- Modify: `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`
  - Remove retired split counters, retired-field helper functions, retired-field risk scoring, retired-field rationale text, and retired-field table columns.
- Modify: `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
  - Make `_current_role()` use only `skill_candidates`; retired fields must not restore removed skills or return compatibility roles.
- Modify: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`
  - Make `_pack_index()` index only `skill_candidates` and `defaults_by_task`; `_current_role()` must not inspect or return compatibility roles.
- Modify: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`
  - Make `_build_pack_index()`, `_current_role()`, `_current_pack_role()`, duplication scoring, and category assignment current-only.

**Runtime-neutral tests**

- Modify: `tests/runtime_neutral/test_global_pack_consolidation_audit.py`
  - Update global audit expectations after removing compat split columns; add retired-only fixture values that must not influence output.
- Modify: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`
  - Add a regression where retired fields mention removed skills, but current roles remain `removed_from_pack`.
- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
  - Remove retired fields from the normal fixture and add a regression proving retired-only bio skills are ignored.
- Modify: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
  - Add regressions proving retired-only ML values do not seed audit rows and do not restore data-ml problem-map roles.

**Do not modify**

- Do not change `config/pack-manifest.json` unless a test exposes a real current-manifest retired-field leak.
- Do not change runtime/router/install behavior.
- Do not introduce a shared helper in this pass.
- Do not split large audit files in this pass.
- Do not install, deploy, push, or mutate host roots under `C:\Users\羽裳\.codex`.

---

### Task 1: Escalate The Terminology Gate From Review To Blocking

**Files:**

- Modify: `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`
- Modify: `config/routing-terminology-hard-cleanup.json`

- [ ] **Step 1: Tighten the hard-cleanup JSON contract test**

In `tests/runtime_neutral/test_routing_terminology_hard_cleanup.py`, update `test_hard_cleanup_scan_reports_json` so the end of the payload assertions requires zero review debt.

Replace the existing lines:

```python
        self.assertGreaterEqual(int(payload["summary"]["review_count"]), 0)
        self.assertEqual([], payload["failures"])
```

with:

```python
        self.assertEqual(0, int(payload["summary"]["review_count"]))
        self.assertEqual([], payload["failures"])
        self.assertEqual([], payload["review"])
```

- [ ] **Step 2: Remove verification-core audit modules from the compatibility-review exception list**

In `config/routing-terminology-hard-cleanup.json`, replace the `compatibility_review_files` list with this exact list:

```json
  "compatibility_review_files": [
    "scripts/runtime/VibeConsultation.Common.ps1",
    "scripts/runtime/legacy/VibeRetiredConsultation.Common.ps1",
    "packages/runtime-core/src/vgo_runtime/router_contract_runtime.py",
    "packages/runtime-core/src/vgo_runtime/router_contract_presentation.py",
    "scripts/router/resolve-pack-route.ps1"
  ],
```

This removes these current verification-core files from review-budget treatment:

```text
packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py
packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py
packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py
packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py
```

- [ ] **Step 3: Run the focused gate test and verify it fails before cleanup**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_routing_terminology_hard_cleanup.py -q
```

Expected: FAIL before Tasks 2-5 are implemented. The failure should come from the hard-cleanup scan reporting current-surface retired-field hits in the four verification-core audit modules, or from `subprocess.CalledProcessError` raised by the scan command returning nonzero.

- [ ] **Step 4: Commit the red gate guard**

```powershell
git add tests\runtime_neutral\test_routing_terminology_hard_cleanup.py config\routing-terminology-hard-cleanup.json
git commit -m "test: make verification-core retired fields blocking"
```

---

### Task 2: Remove Retired Split Fields From Global Pack Consolidation Audit

**Files:**

- Modify: `tests/runtime_neutral/test_global_pack_consolidation_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`

- [ ] **Step 1: Update global audit tests for current-only columns**

In `tests/runtime_neutral/test_global_pack_consolidation_audit.py`, update `test_audit_ranks_high_risk_packs`.

Replace:

```python
        self.assertEqual(0, rows["research-design"].compat_direct_candidate_count)
        self.assertFalse(rows["research-design"].has_compat_role_split)

        self.assertEqual("P0", rows["code-quality"].priority)
        self.assertFalse(rows["code-quality"].has_compat_role_split)
```

with:

```python
        self.assertFalse(hasattr(rows["research-design"], "compat_direct_candidate_count"))
        self.assertFalse(hasattr(rows["research-design"], "compat_stage_candidate_count"))
        self.assertFalse(hasattr(rows["research-design"], "has_compat_role_split"))

        self.assertEqual("P0", rows["code-quality"].priority)
        self.assertFalse(hasattr(rows["code-quality"], "has_compat_role_split"))
```

In `test_artifact_writer_outputs_json_csv_and_markdown`, replace:

```python
        self.assertIn("pack_id,skill_candidate_count,compat_direct_candidate_count", csv_text)
        self.assertIn("research-design", csv_text)
        assert_no_retired_positive_output_terms(csv_text)
```

with:

```python
        self.assertIn("pack_id,skill_candidate_count,default_task_count", csv_text)
        self.assertIn("research-design", csv_text)
        self.assertNotIn("compat_direct_candidate_count", csv_text)
        self.assertNotIn("compat_stage_candidate_count", csv_text)
        self.assertNotIn("has_compat_role_split", csv_text)
        assert_no_retired_positive_output_terms(csv_text)
```

- [ ] **Step 2: Add a retired-only fixture regression to the global audit tests**

Add this test method after `test_artifact_writer_outputs_json_csv_and_markdown`:

```python
    def test_retired_candidate_fields_do_not_influence_global_audit(self) -> None:
        manifest_path = self.root / "config" / "pack-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        research_pack = next(pack for pack in manifest["packs"] if pack["id"] == "research-design")
        research_pack["route_authority_candidates"] = ["retired-only-direct-global"]
        research_pack["stage_assistant_candidates"] = ["retired-only-stage-global"]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        artifact = audit_repository(self.root)
        written = write_artifacts(self.root, artifact, self.root / "outputs" / "skills-audit")
        payload_text = json.dumps(
            {
                "summary": artifact.summary,
                "rows": [row.__dict__ for row in artifact.rows],
            },
            ensure_ascii=False,
        )
        csv_text = written["csv"].read_text(encoding="utf-8")
        markdown_text = written["markdown"].read_text(encoding="utf-8")

        rows = {row.pack_id: row for row in artifact.rows}
        self.assertEqual(7, rows["research-design"].skill_candidate_count)
        for text in (payload_text, csv_text, markdown_text):
            self.assertNotIn("retired-only-direct-global", text)
            self.assertNotIn("retired-only-stage-global", text)
            self.assertNotIn("route_authority_candidates", text)
            self.assertNotIn("stage_assistant_candidates", text)
```

- [ ] **Step 3: Run the global audit tests and verify the current failure**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_global_pack_consolidation_audit.py -q
```

Expected: FAIL before implementation because `PackAuditRow` still exposes compat split attributes and output still contains compat split CSV/Markdown columns.

- [ ] **Step 4: Remove retired split fields from the global audit row schema**

In `packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py`, replace `CSV_FIELDS` with:

```python
CSV_FIELDS = [
    "pack_id",
    "skill_candidate_count",
    "default_task_count",
    "missing_default_skill_count",
    "suspected_overlap_count",
    "broad_keyword_count",
    "tool_primary_risk_count",
    "asset_heavy_candidate_count",
    "risk_score",
    "priority",
    "recommended_next_action",
    "rationale",
]
```

Replace `PackAuditRow` with:

```python
@dataclass(frozen=True)
class PackAuditRow:
    pack_id: str
    skill_candidate_count: int
    default_task_count: int
    missing_default_skill_count: int
    suspected_overlap_count: int
    broad_keyword_count: int
    tool_primary_risk_count: int
    asset_heavy_candidate_count: int
    risk_score: float
    priority: str
    recommended_next_action: str
    rationale: str
```

Delete these helper functions completely:

```python
def _compat_candidates(pack: dict[str, Any], key: str) -> list[str]:
    return [str(item).strip() for item in _as_list(pack.get(key)) if str(item).strip()]


def _has_compat_role_split(pack: dict[str, Any]) -> bool:
    return "route_authority_candidates" in pack or "stage_assistant_candidates" in pack
```

- [ ] **Step 5: Make global risk scoring and rationale current-only**

Replace `_tool_primary_risk_count`, `_recommended_next_action`, `_rationale`, and `_risk_score` with:

```python
def _tool_primary_risk_count(repo_root: Path, pack: dict[str, Any], skill_ids: list[str]) -> int:
    primary_set = set(skill_ids) | set(_defaults(pack).values())
    count = 0
    for skill in sorted(primary_set):
        description = _frontmatter_description(_skill_text(repo_root, skill))
        if _tool_like(skill, description):
            count += 1
    return count


def _recommended_next_action(row: PackAuditRow) -> str:
    if row.priority == "P0":
        return "write a pack-specific problem map before changing skill routing"
    if row.skill_candidate_count >= 5:
        return "define explicit skill-routing boundaries after content review"
    if row.suspected_overlap_count > 0:
        return "review suspected duplicate skills and add route regression probes"
    return "observe; no immediate consolidation pass recommended"


def _rationale(
    *,
    skill_count: int,
    missing_defaults: int,
    overlaps: int,
    broad_keywords: int,
    tool_primary_risk: int,
    asset_heavy: int,
) -> str:
    reasons: list[str] = []
    if skill_count >= 12:
        reasons.append(f"{skill_count} skill candidates")
    elif skill_count >= 5:
        reasons.append(f"{skill_count} skill candidates need explicit boundaries")
    if missing_defaults:
        reasons.append(f"{missing_defaults} defaults point outside candidates")
    if overlaps:
        reasons.append(f"{overlaps} suspected overlap pairs")
    if broad_keywords:
        reasons.append(f"{broad_keywords} shared broad keywords")
    if tool_primary_risk:
        reasons.append(f"{tool_primary_risk} tool-like primary candidates")
    if asset_heavy:
        reasons.append(f"{asset_heavy} candidates with scripts/references/assets")
    return "; ".join(reasons) if reasons else "low structural risk"


def _risk_score(
    *,
    skill_count: int,
    missing_defaults: int,
    overlaps: int,
    broad_keywords: int,
    tool_primary_risk: int,
    asset_heavy: int,
) -> float:
    score = 0.0
    score += min(skill_count * 0.9, 24.0)
    if skill_count >= 5:
        score += 18.0
    score += missing_defaults * 5.0
    score += min(overlaps * 2.2, 22.0)
    score += min(broad_keywords * 1.8, 18.0)
    score += min(tool_primary_risk * 1.2, 15.0)
    score += min(asset_heavy * 0.8, 10.0)
    return round(score, 2)
```

- [ ] **Step 6: Remove retired-field reads from `audit_repository`**

In `audit_repository`, replace the block that computes compat variables, score, rationale, and `PackAuditRow` with this current-only block:

```python
        skills = _skill_candidates(pack)
        defaults = _defaults(pack)
        missing_defaults = sum(1 for skill in defaults.values() if skill not in skills)
        overlaps = _suspected_overlap_count(skills)
        broad_keywords = _broad_keyword_count(keyword_index, routing_rules, skills)
        tool_primary_risk = _tool_primary_risk_count(repo_root, pack, skills)
        asset_heavy = sum(1 for skill in skills if _asset_file_count(repo_root, skill) > 0)
        score = _risk_score(
            skill_count=len(skills),
            missing_defaults=missing_defaults,
            overlaps=overlaps,
            broad_keywords=broad_keywords,
            tool_primary_risk=tool_primary_risk,
            asset_heavy=asset_heavy,
        )
        rationale = _rationale(
            skill_count=len(skills),
            missing_defaults=missing_defaults,
            overlaps=overlaps,
            broad_keywords=broad_keywords,
            tool_primary_risk=tool_primary_risk,
            asset_heavy=asset_heavy,
        )
        provisional = PackAuditRow(
            pack_id=pack_id,
            skill_candidate_count=len(skills),
            default_task_count=len(defaults),
            missing_default_skill_count=missing_defaults,
            suspected_overlap_count=overlaps,
            broad_keyword_count=broad_keywords,
            tool_primary_risk_count=tool_primary_risk,
            asset_heavy_candidate_count=asset_heavy,
            risk_score=score,
            priority="P2",
            recommended_next_action="",
            rationale=rationale,
        )
```

- [ ] **Step 7: Remove compat columns from the global Markdown table**

Replace `_markdown_table` with:

```python
def _markdown_table(rows: list[PackAuditRow]) -> list[str]:
    lines = [
        "| priority | pack | score | skills | defaults | rationale |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {priority} | `{pack}` | {score:.2f} | {skills} | {defaults} | {rationale} |".format(
                priority=row.priority,
                pack=row.pack_id,
                score=row.risk_score,
                skills=row.skill_candidate_count,
                defaults=row.default_task_count,
                rationale=row.rationale.replace("|", "/"),
            )
        )
    return lines
```

- [ ] **Step 8: Run the global audit tests and commit**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_global_pack_consolidation_audit.py -q
```

Expected: PASS.

Commit:

```powershell
git add packages\verification-core\src\vgo_verify\global_pack_consolidation_audit.py tests\runtime_neutral\test_global_pack_consolidation_audit.py
git commit -m "refactor: remove retired split fields from global pack audit"
```

---

### Task 3: Make Code-Quality Current Roles Ignore Retired Fields

**Files:**

- Modify: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`

- [ ] **Step 1: Add a code-quality regression for ignored retired fields**

Add this test method after `test_problem_map_keeps_removed_decisions_visible_after_consolidation`:

```python
    def test_retired_candidate_fields_do_not_restore_removed_code_quality_roles(self) -> None:
        target_candidates = [
            "code-reviewer",
            "deslop",
            "generating-test-reports",
            "receiving-code-review",
            "requesting-code-review",
            "security-reviewer",
            "systematic-debugging",
            "tdd-guide",
            "verification-before-completion",
            "windows-hook-debugging",
        ]
        self._write_json(
            "config/pack-manifest.json",
            {
                "packs": [
                    {
                        "id": "code-quality",
                        "skill_candidates": target_candidates,
                        "route_authority_candidates": ["reviewing-code", "retired-only-code-direct"],
                        "stage_assistant_candidates": ["build-error-resolver", "retired-only-code-stage"],
                        "defaults_by_task": {
                            "debug": "systematic-debugging",
                            "coding": "tdd-guide",
                            "review": "code-reviewer",
                        },
                    }
                ]
            },
        )

        artifact = audit_code_quality_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}
        artifact_text = json.dumps(artifact.to_dict(), ensure_ascii=False)

        self.assertEqual("removed_from_pack", rows["reviewing-code"].current_role)
        self.assertEqual("removed_from_pack", rows["build-error-resolver"].current_role)
        self.assertNotIn("retired-only-code-direct", rows)
        self.assertNotIn("retired-only-code-stage", rows)
        self.assertNotIn("compat_direct_candidate", artifact_text)
        self.assertNotIn("compat_stage_candidate", artifact_text)
        self.assertNotIn("retired-only-code-direct", artifact_text)
        self.assertNotIn("retired-only-code-stage", artifact_text)
```

- [ ] **Step 2: Run the code-quality tests and verify the current failure**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py -q
```

Expected: FAIL before implementation because `_current_role()` still reads the retired fields and returns `compat_direct_candidate` or `compat_stage_candidate` for removed skills named only by retired fields.

- [ ] **Step 3: Make `_current_role()` current-only**

In `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`, replace `_current_role` with:

```python
def _current_role(skill_id: str, pack: dict[str, Any]) -> str:
    skill_candidates = {str(item) for item in _as_list(pack.get("skill_candidates"))}
    if skill_id not in skill_candidates:
        return "removed_from_pack"
    return "candidate"
```

- [ ] **Step 4: Run code-quality tests and commit**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py -q
```

Expected: PASS.

Commit:

```powershell
git add packages\verification-core\src\vgo_verify\code_quality_pack_consolidation_audit.py tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py
git commit -m "refactor: ignore retired fields in code quality audit"
```

---

### Task 4: Make Bio-Science Pack Index Current-Only

**Files:**

- Modify: `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`

- [ ] **Step 1: Remove retired fields from the normal bio-science fixture**

In `tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py`, remove these lines from the `bio-science` fixture in `_write_fixture_repo`:

```python
                        "route_authority_candidates": BIO_SCIENCE_DIRECT_ROUTE_OWNERS,
                        "stage_assistant_candidates": [],
```

Keep this current field unchanged:

```python
                        "skill_candidates": BIO_SCIENCE_DIRECT_OWNERS,
```

- [ ] **Step 2: Add a bio-science regression for ignored retired fields**

Add this test method after `test_removed_skills_are_merge_delete_rows`:

```python
    def test_retired_candidate_fields_do_not_add_bio_rows_or_roles(self) -> None:
        manifest_path = self.root / "config" / "pack-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bio_pack = next(pack for pack in manifest["packs"] if pack["id"] == "bio-science")
        bio_pack["route_authority_candidates"] = ["retired-only-bio-direct"]
        bio_pack["stage_assistant_candidates"] = ["pysam", "retired-only-bio-stage"]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        artifact = audit_bio_science_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}
        artifact_text = json.dumps(artifact.to_dict(), ensure_ascii=False)

        self.assertNotIn("retired-only-bio-direct", rows)
        self.assertNotIn("retired-only-bio-stage", rows)
        self.assertEqual("candidate", rows["pysam"].current_role)
        self.assertEqual("merge-delete-after-migration", rows["pysam"].target_role)
        self.assertNotIn("compat_direct_candidate", artifact_text)
        self.assertNotIn("compat_stage_candidate", artifact_text)
        self.assertNotIn("retired-only-bio-direct", artifact_text)
        self.assertNotIn("retired-only-bio-stage", artifact_text)
```

- [ ] **Step 3: Run the bio-science tests and verify the current failure**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py -q
```

Expected: FAIL before implementation because `_pack_index()` still indexes retired fields and `_current_role()` still returns compatibility roles.

- [ ] **Step 4: Make the bio-science pack index current-only**

In `packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py`, replace `_pack_index` and `_current_role` with:

```python
def _pack_index(pack_manifest: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    index: dict[str, dict[str, set[str]]] = {}
    for pack in _as_list(pack_manifest.get("packs")):
        if not isinstance(pack, dict):
            continue
        pack_id = str(pack.get("id", "")).strip()
        if not pack_id:
            continue
        for value in _as_list(pack.get("skill_candidates")):
            skill_id = str(value).strip()
            if not skill_id:
                continue
            record = index.setdefault(skill_id, {"packs": set(), "defaults": set()})
            record["packs"].add(pack_id)
        defaults_by_task = pack.get("defaults_by_task")
        if isinstance(defaults_by_task, dict):
            for value in defaults_by_task.values():
                skill_id = str(value).strip()
                if not skill_id:
                    continue
                record = index.setdefault(skill_id, {"packs": set(), "defaults": set()})
                record["packs"].add(pack_id)
                record["defaults"].add(pack_id)
    return index


def _current_role(record: dict[str, set[str]]) -> str:
    if record["defaults"]:
        return "default"
    return "candidate"
```

In `audit_bio_science_problem_map`, replace the default record passed to `pack_index.get(...)` with:

```python
        record = pack_index.get(skill_id, {"packs": set(), "defaults": set()})
```

- [ ] **Step 5: Run bio-science tests and commit**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py -q
```

Expected: PASS.

Commit:

```powershell
git add packages\verification-core\src\vgo_verify\bio_science_pack_consolidation_audit.py tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py
git commit -m "refactor: ignore retired fields in bio science audit"
```

---

### Task 5: Make ML Skills Pruning Current-Only

**Files:**

- Modify: `tests/runtime_neutral/test_ml_skills_pruning_audit.py`
- Modify: `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`

- [ ] **Step 1: Add an ML audit regression for ignored retired-only rows**

Add this test method after `test_audit_keeps_or_defers_owner_and_specialist_skills`:

```python
    def test_retired_candidate_fields_do_not_seed_ml_audit_rows(self) -> None:
        manifest_path = self.root / "config" / "pack-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        data_ml_pack = next(pack for pack in manifest["packs"] if pack["id"] == "data-ml")
        data_ml_pack["route_authority_candidates"] = ["retired-only-direct-ml"]
        data_ml_pack["stage_assistant_candidates"] = [
            "training-machine-learning-models",
            "retired-only-stage-ml",
        ]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        artifact = audit_repository(self.root)
        rows = {row.skill_id: row for row in artifact.rows}
        artifact_text = json.dumps(artifact.to_dict(), ensure_ascii=False)

        self.assertNotIn("retired-only-direct-ml", rows)
        self.assertNotIn("retired-only-stage-ml", rows)
        self.assertEqual("candidate", rows["training-machine-learning-models"].current_role)
        self.assertNotIn("compat_direct_candidate", artifact_text)
        self.assertNotIn("compat_stage_candidate", artifact_text)
        self.assertNotIn("retired-only-direct-ml", artifact_text)
        self.assertNotIn("retired-only-stage-ml", artifact_text)
```

- [ ] **Step 2: Add a data-ml problem-map regression for ignored retired fields**

Add this test method after `test_data_ml_problem_map_marks_targets_for_consolidation`:

```python
    def test_retired_candidate_fields_do_not_restore_data_ml_problem_roles(self) -> None:
        self._write_json(
            "config/pack-manifest.json",
            {
                "packs": [
                    {
                        "id": "data-ml",
                        "skill_candidates": [
                            "scikit-learn",
                            "shap",
                        ],
                        "route_authority_candidates": ["training-machine-learning-models"],
                        "stage_assistant_candidates": [
                            "preprocessing-data-with-automated-pipelines",
                            "retired-only-data-ml-stage",
                        ],
                        "defaults_by_task": {
                            "planning": "scikit-learn",
                            "coding": "scikit-learn",
                        },
                    }
                ]
            },
        )

        artifact = audit_data_ml_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}
        artifact_text = json.dumps(artifact.to_dict(), ensure_ascii=False)

        self.assertEqual("removed_from_pack", rows["training-machine-learning-models"].current_role)
        self.assertEqual("removed_from_pack", rows["preprocessing-data-with-automated-pipelines"].current_role)
        self.assertNotIn("retired-only-data-ml-stage", rows)
        self.assertNotIn("compat_direct_candidate", artifact_text)
        self.assertNotIn("compat_stage_candidate", artifact_text)
        self.assertNotIn("retired-only-data-ml-stage", artifact_text)
```

- [ ] **Step 3: Run ML tests and verify the current failure**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_ml_skills_pruning_audit.py -q
```

Expected: FAIL before implementation because `_build_pack_index()` and `_current_pack_role()` still read retired fields, and role/category logic still emits compatibility roles.

- [ ] **Step 4: Replace the ML pack index and current-role helpers**

In `packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py`, replace `_build_pack_index`, `_current_role`, and `_current_pack_role` with:

```python
def _build_pack_index(pack_manifest: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    index: dict[str, dict[str, set[str]]] = {}
    for pack in _as_list(pack_manifest.get("packs")):
        if not isinstance(pack, dict):
            continue
        pack_id = str(pack.get("id", "")).strip()
        if not pack_id:
            continue
        defaults = {str(item).strip() for item in _flatten_text(pack.get("defaults_by_task")).split() if item}
        for value in _as_list(pack.get("skill_candidates")):
            skill_id = str(value).strip()
            if skill_id:
                record = index.setdefault(skill_id, {"packs": set(), "defaults": set()})
                record["packs"].add(pack_id)
        defaults_by_task = pack.get("defaults_by_task")
        if isinstance(defaults_by_task, dict):
            for value in defaults_by_task.values():
                skill_id = str(value).strip()
                if skill_id:
                    record = index.setdefault(skill_id, {"packs": set(), "defaults": set()})
                    record["packs"].add(pack_id)
                    record["defaults"].add(pack_id)
        elif defaults:
            for skill_id in defaults:
                record = index.setdefault(skill_id, {"packs": set(), "defaults": set()})
                record["packs"].add(pack_id)
                record["defaults"].add(pack_id)
    return index


def _current_role(record: dict[str, set[str]]) -> str:
    if record["defaults"]:
        return "default"
    return "candidate"


def _current_pack_role(skill_id: str, pack: dict[str, Any]) -> str:
    skill_candidates = {str(item).strip() for item in _as_list(pack.get("skill_candidates"))}
    defaults_by_task = pack.get("defaults_by_task")
    default_skills = (
        {str(value).strip() for value in defaults_by_task.values() if str(value).strip()}
        if isinstance(defaults_by_task, dict)
        else set()
    )
    if skill_id in default_skills:
        return "default"
    if skill_id not in skill_candidates:
        return "removed_from_pack"
    return "candidate"
```

- [ ] **Step 5: Remove compatibility role branches from ML scoring and category logic**

In `_make_row`, replace the default record fallback with:

```python
    record = pack_index.get(skill_id, {"packs": set(), "defaults": set()})
```

In `_duplication_score`, delete this branch:

```python
    if current_role == "compat_stage_candidate" and len(text) < 3500 and skill_id in DEFAULT_REPLACEMENTS:
        return 4
```

Then make the replacement-skill branch handle generic current candidates by replacing:

```python
    if skill_id in DEFAULT_REPLACEMENTS and not has_scripts and not has_references:
        return 5
```

with:

```python
    if skill_id in DEFAULT_REPLACEMENTS and not has_scripts and not has_references:
        return 5
    if current_role == "candidate" and len(text) < 3500 and skill_id in DEFAULT_REPLACEMENTS:
        return 4
```

Replace `_category` with:

```python
def _category(skill_id: str, recommended_action: str, current_role: str) -> str:
    if recommended_action == "delete":
        return "删除候选"
    if skill_id in SPECIALIST_DEFER_SKILLS:
        return "工具型"
    if skill_id in OWNER_SKILLS:
        return "主专家"
    if current_role == "default":
        return "默认技能"
    return "参考型"
```

- [ ] **Step 6: Run ML tests and commit**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_ml_skills_pruning_audit.py -q
```

Expected: PASS.

Commit:

```powershell
git add packages\verification-core\src\vgo_verify\ml_skills_pruning_audit.py tests\runtime_neutral\test_ml_skills_pruning_audit.py
git commit -m "refactor: ignore retired fields in ml pruning audit"
```

---

### Task 6: Run Final Gates And Regression Sweep

**Files:**

- Verify all files modified by Tasks 1-5.

- [ ] **Step 1: Run the focused runtime-neutral audit tests**

Run:

```powershell
python -m pytest tests\runtime_neutral\test_routing_terminology_hard_cleanup.py tests\runtime_neutral\test_global_pack_consolidation_audit.py tests\runtime_neutral\test_code_quality_pack_consolidation_audit.py tests\runtime_neutral\test_bio_science_pack_consolidation_audit.py tests\runtime_neutral\test_ml_skills_pruning_audit.py -q
```

Expected: PASS.

- [ ] **Step 2: Verify retired fields no longer appear in targeted current audit modules**

Run:

```powershell
rg "route_authority_candidates|stage_assistant_candidates" packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py
```

Expected: no output and exit code `1`, which is ripgrep's normal no-match status.

Run:

```powershell
rg "compat_direct|compat_stage|compat_direct_candidate|compat_stage_candidate|has_compat_role_split" packages/verification-core/src/vgo_verify/global_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/bio_science_pack_consolidation_audit.py packages/verification-core/src/vgo_verify/ml_skills_pruning_audit.py
```

Expected: no output and exit code `1`.

- [ ] **Step 3: Run terminology and routing debt gates**

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-routing-terminology-hard-cleanup-scan.ps1 -Json
```

Expected JSON fields:

```json
{
  "status": "pass",
  "summary": {
    "fail_count": 0,
    "review_count": 0
  },
  "failures": [],
  "review": []
}
```

Run:

```powershell
powershell -NoLogo -NoProfile -File scripts\verify\vibe-current-routing-debt-gate.ps1 -Json
```

Expected: `status` is `pass`, and the summary reports `P0 = 0`, `P1 = 0`, and `P2 = 0`.

- [ ] **Step 4: Run the wider regression suite**

Run:

```powershell
python -m pytest tests\contract tests\unit tests\runtime_neutral -q
```

Expected: PASS.

- [ ] **Step 5: Run whitespace and diff checks**

Run:

```powershell
git diff --check
git status --short --branch
```

Expected:

```text
git diff --check
```

prints no output. `git status --short --branch` shows only the intended implementation branch commits or a clean working tree after the final commit.

- [ ] **Step 6: Commit final verification notes if any test-only adjustments were required**

If Tasks 1-5 already committed all code and tests, skip this commit. If Task 6 required only narrow test expectation fixes, commit them:

```powershell
git add packages\verification-core\src\vgo_verify tests\runtime_neutral config\routing-terminology-hard-cleanup.json
git commit -m "test: verify verification-core retired field erasure"
```

---

## Success Criteria

The implementation is complete when all of these are true:

- `vibe-routing-terminology-hard-cleanup-scan.ps1 -Json` reports `status: pass`.
- `summary.fail_count == 0`.
- `summary.review_count == 0`.
- `review == []`.
- `rg "route_authority_candidates|stage_assistant_candidates" ...` has no hits in the four targeted audit modules.
- `rg "compat_direct|compat_stage|compat_direct_candidate|compat_stage_candidate|has_compat_role_split" ...` has no hits in the four targeted audit modules.
- Old fixture values supplied only through retired fields cannot influence audit rows or generated JSON/CSV/Markdown output.
- `vibe-current-routing-debt-gate.ps1 -Json` remains `P0/P1/P2 = 0/0/0`.
- `python -m pytest tests\contract tests\unit tests\runtime_neutral -q` passes.
- No install, deployment, push, or host-root mutation happens.

## Rollback

- Revert Task 1 if the terminology gate escalation itself is incorrect.
- Revert Task 2 if global pack audit priority or report schema changes break downstream consumers.
- Revert Task 3 if code-quality problem-map roles regress.
- Revert Task 4 if bio-science problem-map rows or target counts regress.
- Revert Task 5 if ML audit pruning decisions or problem-map roles regress.
- No rollback path should require touching runtime, router, installer, deployment, or `C:\Users\羽裳\.codex`.
