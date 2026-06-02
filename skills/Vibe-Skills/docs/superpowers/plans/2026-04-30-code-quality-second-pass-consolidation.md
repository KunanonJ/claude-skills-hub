# Code-Quality Second-Pass Consolidation Implementation Plan

> Historical / Retired Note: This document discusses retired or cleanup-context routing terminology. The current routing model is `skill_candidates -> skill_routing.selected -> selected_skill_execution -> skill_usage`; old terms here are historical only and are not current runtime states.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the second-pass `code-quality` consolidation by preserving the 10 direct route owners, deleting low-value legacy skill directories after migration, removing stale helper-expert wording, and proving the routing surface stays simple.

**Architecture:** Keep the current simplified routing contract: `candidate skill -> selected skill -> used / unused`. Add failing tests for the second-pass target state first, update the code-quality audit map and governance text, migrate the useful `code-review` assets into `code-reviewer`, physically delete safe legacy directories, clean live stale references, refresh the skills lock, and verify with focused and broad gates.

**Tech Stack:** Python unittest/pytest, PowerShell verification scripts, JSON config, Markdown governance docs, existing `bundled/skills` layout.

---

## File Structure

- Modify: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`
  - Adds second-pass assertions for legacy directory pruning, migrated `code-reviewer` assets, zero stage-assistant wording, and retained `error-resolver` migration deferral.
- Modify: `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
  - Updates target decisions for `debugging-strategies`, `code-review-excellence`, `code-review`, and `error-resolver`.
  - Updates artifact summary and Markdown headings so the current output does not present a live stage-assistant section.
- Modify: `bundled/skills/code-reviewer/SKILL.md`
  - Records the migrated legacy style-guide and checker assets.
- Move: `bundled/skills/code-review/references/style-guide.md` -> `bundled/skills/code-reviewer/references/python-style-guide.md`
  - Keeps the useful Python style reference under the surviving direct owner.
- Move: `bundled/skills/code-review/scripts/check_style.py` -> `bundled/skills/code-reviewer/scripts/check_style.py`
  - Keeps the lightweight style-check helper under the surviving direct owner.
- Delete: `bundled/skills/code-review/`
  - Removed after its useful assets are migrated.
- Delete: `bundled/skills/debugging-strategies/`
  - Removed because it overlaps `systematic-debugging` and has no unique asset subdirectories.
- Delete: `bundled/skills/code-review-excellence/`
  - Removed because it is broad review-culture/training material and should not be a routed expert.
- Keep: `bundled/skills/error-resolver/`
  - Retained because it has substantial `analysis/`, `patterns/`, and `replay/` assets.
- Modify as found by search: active references under `config/`, `scripts/`, `bundled/skills/`
  - Replaces live references to deleted skill IDs with current owners or removes old scheduling examples.
- Modify: `docs/governance/code-quality-problem-first-consolidation-2026-04-27.md`
  - Marks the previous stage-assistant wording as historical and points to the second-pass note.
- Create: `docs/governance/code-quality-second-pass-consolidation-2026-04-30.md`
  - Records the final second-pass state and verification evidence.
- Modify generated: `config/skills-lock.json`
  - Refreshed after physical directory deletion.
- Optional generated: `outputs/skills-audit/code-quality-problem-map.json`
- Optional generated: `outputs/skills-audit/code-quality-problem-map.csv`
- Optional generated: `outputs/skills-audit/code-quality-problem-consolidation.md`

## Execution Boundaries

- Do not change the six-stage Vibe runtime.
- Do not restore `stage_assistant_candidates`.
- Do not create helper-expert, advisory, consultation, primary/secondary, or main/sub skill states.
- Do not delete `error-resolver` in this pass.
- Do not claim material skill use in an actual Vibe task. This pass proves routing/config/bundled skill cleanup only.
- Do not edit unrelated packs except stale live references that point from those packs to deleted code-quality skills.

## Task 1: Add Failing Second-Pass Tests

**Files:**
- Modify: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`

- [ ] **Step 1: Add tests for second-pass target roles**

Append these methods inside `CodeQualityPackConsolidationAuditTests` before `if __name__ == "__main__":`.

```python
    def test_second_pass_marks_legacy_directories_for_pruning_or_deferral(self) -> None:
        artifact = audit_code_quality_problem_map(self.root)
        rows = {row.skill_id: row for row in artifact.rows}

        self.assertEqual("merge-delete-after-migration", rows["code-review"].target_role)
        self.assertFalse(rows["code-review"].delete_allowed_now)
        self.assertEqual("code-reviewer", rows["code-review"].target_owner)

        self.assertEqual("delete", rows["debugging-strategies"].target_role)
        self.assertTrue(rows["debugging-strategies"].delete_allowed_now)
        self.assertEqual("systematic-debugging", rows["debugging-strategies"].target_owner)

        self.assertEqual("delete", rows["code-review-excellence"].target_role)
        self.assertTrue(rows["code-review-excellence"].delete_allowed_now)
        self.assertEqual("code-reviewer", rows["code-review-excellence"].target_owner)

        self.assertEqual("defer-migration", rows["error-resolver"].target_role)
        self.assertFalse(rows["error-resolver"].delete_allowed_now)
        self.assertEqual("systematic-debugging", rows["error-resolver"].target_owner)
```

- [ ] **Step 2: Add real-repo asset migration and deletion assertions**

Append this method in the same class.

```python
    def test_real_repo_migrates_code_review_assets_and_removes_deleted_directories(self) -> None:
        code_reviewer_root = REPO_ROOT / "bundled" / "skills" / "code-reviewer"

        self.assertTrue((code_reviewer_root / "references" / "python-style-guide.md").exists())
        self.assertTrue((code_reviewer_root / "scripts" / "check_style.py").exists())

        for deleted_skill in [
            "code-review",
            "debugging-strategies",
            "code-review-excellence",
        ]:
            with self.subTest(deleted_skill=deleted_skill):
                self.assertFalse((REPO_ROOT / "bundled" / "skills" / deleted_skill).exists())

        self.assertTrue((REPO_ROOT / "bundled" / "skills" / "error-resolver").exists())
```

- [ ] **Step 3: Add artifact wording assertion**

Append this method in the same class.

```python
    def test_problem_artifact_does_not_describe_live_stage_assistants(self) -> None:
        artifact = audit_code_quality_problem_map(self.root)
        written = write_code_quality_problem_artifacts(
            self.root,
            artifact,
            self.root / "outputs" / "skills-audit",
        )

        markdown_text = written["markdown"].read_text(encoding="utf-8")
        self.assertNotIn("## 阶段助手", markdown_text)
        self.assertIn("## 保留直接路由", markdown_text)
        self.assertIn("## 迁移后删除", markdown_text)
        self.assertIn("## 推迟迁移", markdown_text)
```

- [ ] **Step 4: Update old expectations in existing tests**

In `test_problem_map_marks_safe_delete_and_move_out`, keep the existing `reviewing-code`, `build-error-resolver`, and `error-resolver` assertions, but replace the final `error-resolver` target-role assertion with:

```python
        self.assertEqual("defer-migration", rows["error-resolver"].target_role)
        self.assertFalse(rows["error-resolver"].delete_allowed_now)
        self.assertIn("assets=1", rows["error-resolver"].unique_assets)
```

In `test_problem_map_keeps_removed_decisions_visible_after_consolidation`, replace:

```python
        self.assertEqual("move-out", rows["code-review"].target_role)
```

with:

```python
        self.assertEqual("merge-delete-after-migration", rows["code-review"].target_role)
```

In `test_artifact_writer_outputs_json_csv_and_markdown`, replace:

```python
        self.assertIn("## 保留主路由", markdown_text)
```

with:

```python
        self.assertIn("## 保留直接路由", markdown_text)
```

- [ ] **Step 5: Run focused tests and confirm failure**

```powershell
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py -q
```

Expected now: FAIL. Failures should mention missing `python-style-guide.md`, existing legacy directories, old target roles such as `move-out`, and the old `## 阶段助手` artifact heading.

- [ ] **Step 6: Commit failing tests**

```powershell
git add tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py
git commit -m "test: capture code quality second pass targets"
```

## Task 2: Update The Code-Quality Audit Map

**Files:**
- Modify: `packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py`
- Test: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`

- [ ] **Step 1: Replace the legacy decisions**

In `CODE_QUALITY_DECISIONS`, replace the dictionaries for `code-review`, `debugging-strategies`, `error-resolver`, and `code-review-excellence` with these exact entries.

```python
    "code-review": {
        "problem_ids": ["code_review_general"],
        "primary_problem_id": "code_review_general",
        "target_role": "merge-delete-after-migration",
        "target_owner": "code-reviewer",
        "overlap_with": "code-reviewer; reviewing-code",
        "routing_change": "migrate style guide and checker into code-reviewer, then delete legacy directory",
        "delete_allowed_now": False,
        "risk_level": "medium",
        "rationale": "与 code-reviewer 重叠；style guide 和 check_style.py 先迁移到 code-reviewer 后再删除目录。",
    },
    "debugging-strategies": {
        "problem_ids": ["debug_root_cause"],
        "primary_problem_id": "debug_root_cause",
        "target_role": "delete",
        "target_owner": "systematic-debugging",
        "overlap_with": "systematic-debugging; error-resolver",
        "routing_change": "delete legacy debugging strategy wrapper after stale-reference cleanup",
        "delete_allowed_now": True,
        "risk_level": "low",
        "rationale": "和 systematic-debugging 重叠，且只有 SKILL.md；不保留为独立路由专家。",
    },
    "error-resolver": {
        "problem_ids": ["debug_root_cause"],
        "primary_problem_id": "debug_root_cause",
        "target_role": "defer-migration",
        "target_owner": "systematic-debugging",
        "overlap_with": "systematic-debugging; debugging-strategies",
        "routing_change": "remove active routing hints but keep directory for a separate asset migration pass",
        "delete_allowed_now": False,
        "risk_level": "high",
        "rationale": "资产重，包含 analysis、patterns 和 replay 内容；本轮只清理活跃路由暗示，不物理删除。",
    },
    "code-review-excellence": {
        "problem_ids": ["review_training_standards"],
        "primary_problem_id": "review_training_standards",
        "target_role": "delete",
        "target_owner": "code-reviewer",
        "overlap_with": "code-reviewer",
        "routing_change": "delete broad review-culture wrapper after stale-reference cleanup",
        "delete_allowed_now": True,
        "risk_level": "low",
        "rationale": "偏 review 文化、标准、教学，和 code-reviewer 的直接审查入口重叠，不保留独立专家。",
    },
```

- [ ] **Step 2: Update artifact summary counts**

In `ProblemMapArtifact.to_dict`, inside the `"summary"` dictionary, add these two keys immediately after `"move_out_count"`:

```python
                "merge_delete_after_migration_count": sum(
                    1 for row in self.rows if row.target_role == "merge-delete-after-migration"
                ),
                "defer_migration_count": sum(1 for row in self.rows if row.target_role == "defer-migration"),
```

Keep the existing keys. Do not remove `move_out_count`; it is still useful for historical fixture coverage.

- [ ] **Step 3: Replace Markdown artifact sections**

In `_write_markdown`, replace the current body-building logic with this version.

```python
def _write_markdown(path: Path, artifact: ProblemMapArtifact) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keep_rows = [row for row in artifact.rows if row.target_role == "keep-route-authority"]
    delete_rows = [row for row in artifact.rows if row.target_role == "delete"]
    merge_delete_rows = [
        row for row in artifact.rows if row.target_role == "merge-delete-after-migration"
    ]
    defer_rows = [row for row in artifact.rows if row.target_role == "defer-migration"]
    move_rows = [row for row in artifact.rows if row.target_role == "move-out"]
    text = "\n".join(
        [
            "# Code-Quality Problem-First Consolidation",
            "",
            f"generated_at: `{artifact.generated_at}`",
            "",
            "Current routing model: `candidate skill -> selected skill -> used / unused`.",
            "",
            "## 保留直接路由",
            "",
            _markdown_table(keep_rows),
            "",
            "## 删除候选",
            "",
            _markdown_table(delete_rows),
            "",
            "## 迁移后删除",
            "",
            _markdown_table(merge_delete_rows),
            "",
            "## 推迟迁移",
            "",
            _markdown_table(defer_rows),
            "",
            "## 已移出 code-quality 但保留目录",
            "",
            _markdown_table(move_rows),
            "",
        ]
    )
    path.write_text(text, encoding="utf-8")
```

- [ ] **Step 4: Run focused tests and confirm partial progress**

```powershell
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py -q
```

Expected now: still FAIL only on real-repo file-system assertions for asset migration and deleted directories. Target-role and artifact-heading failures should be resolved.

- [ ] **Step 5: Commit audit-map update**

```powershell
git add packages/verification-core/src/vgo_verify/code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py
git commit -m "fix: update code quality second pass audit targets"
```

## Task 3: Migrate `code-review` Assets Into `code-reviewer`

**Files:**
- Move: `bundled/skills/code-review/references/style-guide.md`
- Move: `bundled/skills/code-review/scripts/check_style.py`
- Modify: `bundled/skills/code-reviewer/SKILL.md`
- Delete after migration: `bundled/skills/code-review/`
- Test: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`

- [ ] **Step 1: Move the useful reference asset**

```powershell
git mv bundled\skills\code-review\references\style-guide.md bundled\skills\code-reviewer\references\python-style-guide.md
```

Expected: `bundled/skills/code-reviewer/references/python-style-guide.md` exists and the old `style-guide.md` path is staged as removed.

- [ ] **Step 2: Move the useful checker script**

```powershell
git mv bundled\skills\code-review\scripts\check_style.py bundled\skills\code-reviewer\scripts\check_style.py
```

Expected: `bundled/skills/code-reviewer/scripts/check_style.py` exists and the old checker path is staged as removed.

- [ ] **Step 3: Update `code-reviewer` documentation**

In `bundled/skills/code-reviewer/SKILL.md`, add this section after the `## Routing Boundary` block and before `## Quick Start`.

```markdown
## Migrated Legacy Assets

The legacy `code-review` wrapper has been absorbed into this direct route owner.

- `references/python-style-guide.md` contains the retained Python naming, import, documentation, error-handling, and secret-handling guidance.
- `scripts/check_style.py` is a lightweight stdin/string style checker for quick local review support.

Use these assets as supporting material inside `code-reviewer`; do not route to the deleted `code-review` skill.
```

- [ ] **Step 4: Remove the empty legacy wrapper directory**

After Steps 1 and 2, the old directory should only contain `SKILL.md` and empty subdirectories. Remove the directory.

```powershell
Remove-Item -LiteralPath bundled\skills\code-review -Recurse
```

Expected: `Test-Path bundled\skills\code-review` returns `False`.

- [ ] **Step 5: Run focused tests**

```powershell
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py -q
```

Expected now: FAIL only for `debugging-strategies` and `code-review-excellence` still existing, unless later tasks have already deleted them.

- [ ] **Step 6: Commit migration**

```powershell
git add bundled/skills/code-reviewer bundled/skills/code-review tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py
git commit -m "fix: merge legacy code review assets into code reviewer"
```

## Task 4: Delete Low-Value Legacy Directories

**Files:**
- Delete: `bundled/skills/debugging-strategies/`
- Delete: `bundled/skills/code-review-excellence/`
- Test: `tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py`

- [ ] **Step 1: Confirm both directories have no asset subdirectories**

```powershell
Get-ChildItem -LiteralPath bundled\skills\debugging-strategies -Recurse -File | Select-Object FullName
Get-ChildItem -LiteralPath bundled\skills\code-review-excellence -Recurse -File | Select-Object FullName
```

Expected before deletion:

```text
bundled\skills\debugging-strategies\SKILL.md
bundled\skills\code-review-excellence\SKILL.md
```

If additional files appear, stop and inspect them before deletion.

- [ ] **Step 2: Remove `debugging-strategies`**

```powershell
Remove-Item -LiteralPath bundled\skills\debugging-strategies -Recurse
```

Expected: `Test-Path bundled\skills\debugging-strategies` returns `False`.

- [ ] **Step 3: Remove `code-review-excellence`**

```powershell
Remove-Item -LiteralPath bundled\skills\code-review-excellence -Recurse
```

Expected: `Test-Path bundled\skills\code-review-excellence` returns `False`.

- [ ] **Step 4: Verify `error-resolver` remains**

```powershell
Test-Path bundled\skills\error-resolver
```

Expected:

```text
True
```

- [ ] **Step 5: Run focused tests**

```powershell
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py -q
```

Expected: PASS for the focused code-quality audit tests, unless stale live references still need tests from later tasks.

- [ ] **Step 6: Commit physical deletion**

```powershell
git add bundled/skills/debugging-strategies bundled/skills/code-review-excellence tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py
git commit -m "fix: remove legacy code quality wrappers"
```

## Task 5: Remove Stale Live References To Deleted Skills

**Files:**
- Modify as needed: `config/skill-routing-rules.json`
- Modify as needed: `config/skill-keyword-index.json`
- Modify as needed: `config/capability-catalog.json`
- Modify as needed: `bundled/skills/autonomous-builder/SKILL.md`
- Modify as needed: `bundled/skills/autonomous-builder/references/skill-scheduling.md`
- Modify as needed: `bundled/skills/spec-kit-vibe-compat/command-map.json`
- Modify as needed: `bundled/skills/superclaude-framework-compat/command-map.json`
- Modify as needed: `bundled/skills/think-harder/SKILL.md`
- Modify as needed: `scripts/verify/vibe-pack-regression-matrix.ps1`
- Modify as needed: `scripts/verify/vibe-soft-migration-practice.ps1`
- Modify as needed: `scripts/verify/vibe-openspec-governance-gate.ps1`

- [ ] **Step 1: Run the stale-reference search**

```powershell
rg -n -P "\b(code-review|debugging-strategies|code-review-excellence)\b" config scripts bundled
```

Expected before cleanup: references appear in active configs, scripts, and bundled skill text.

- [ ] **Step 2: Remove deleted IDs from active routing rules**

In `config/skill-routing-rules.json`, remove the top-level entries for:

```text
code-review
debugging-strategies
code-review-excellence
```

If `error-resolver` still has a top-level routing entry, remove that entry too. The directory remains, but it should not be an active direct route owner in this pass.

- [ ] **Step 3: Replace active bundled skill scheduling examples**

Use these substitutions in active bundled skill text:

| Old text | Replacement |
|---|---|
| `code-review` as a skill ID | `code-reviewer` |
| `code-review-excellence` as a skill ID | `code-reviewer` |
| `debugging-strategies` as a skill ID | `systematic-debugging` |
| `error-resolver` as a scheduled/invoked route | `systematic-debugging` |

Keep `error-resolver` only when the text explicitly explains retained legacy assets or deferred migration.

Concrete expected edits:

- In `bundled/skills/autonomous-builder/references/skill-scheduling.md`, category mappings should list `code-reviewer` for code review and `systematic-debugging` for debugging.
- In `bundled/skills/autonomous-builder/SKILL.md`, scheduling tables should not recommend deleted code-quality skill IDs.
- In `bundled/skills/spec-kit-vibe-compat/command-map.json`, replace `"code-review"` in `codex_skills` with `"code-reviewer"`.
- In `bundled/skills/think-harder/SKILL.md`, replace "pair with `code-review`" with "pair with `code-reviewer`".

- [ ] **Step 4: Update verification scripts using deleted requested-skill IDs**

In `scripts/verify/vibe-pack-regression-matrix.ps1`, replace:

```powershell
RequestedSkill = "code-review"
```

with:

```powershell
RequestedSkill = "code-reviewer"
```

where the test is about the canonical code-quality review route.

In `scripts/verify/vibe-soft-migration-practice.ps1`, either update the practice to use `code-reviewer` as the canonical skill, or move the old alias assertion into a clearly legacy-only compatibility check that does not require a live `bundled/skills/code-review` directory.

In `scripts/verify/vibe-openspec-governance-gate.ps1`, replace requested-skill references to deleted `code-review` with `code-reviewer`.

- [ ] **Step 5: Re-run stale-reference search**

```powershell
rg -n -P "\b(code-review|debugging-strategies|code-review-excellence)\b" config scripts bundled
```

Expected after cleanup: no matches in active `config`, `scripts`, or `bundled` files, except legacy whitelist entries that explicitly test alias compatibility and do not require the deleted skill directory.

- [ ] **Step 6: Commit stale-reference cleanup**

```powershell
git add config scripts bundled
git commit -m "fix: clear stale code quality skill references"
```

## Task 6: Update Governance Documentation

**Files:**
- Modify: `docs/governance/code-quality-problem-first-consolidation-2026-04-27.md`
- Create: `docs/governance/code-quality-second-pass-consolidation-2026-04-30.md`

- [ ] **Step 1: Mark the old governance note as historical**

At the top of `docs/governance/code-quality-problem-first-consolidation-2026-04-27.md`, after the date, add:

```markdown
> Historical note: this document records the 2026-04-27 first-pass state. The current 2026-04-30 second-pass state has `stage_assistant_candidates = 0`, and `requesting-code-review` is a direct route owner for review-request preparation. See `docs/governance/code-quality-second-pass-consolidation-2026-04-30.md`.
```

Then update the "调整前后" table to include a "2026-04-30 当前状态" column:

```markdown
| 项目 | 2026-04-27 调整前 | 2026-04-27 调整后 | 2026-04-30 当前状态 |
|---|---:|---:|---:|
| `skill_candidates` | 16 | 10 | 10 |
| `route_authority_candidates` | 0 | 9 | 10 |
| `stage_assistant_candidates` | 0 | 1 | 0 |
| 物理删除目录 | 0 | 2 | 3 second-pass deletions; 1 deferred migration |
```

Replace the old `## 阶段助手` section with:

```markdown
## 2026-04-30 更新：不再使用阶段助手

`requesting-code-review` 已经改为直接 route owner，负责准备发起 code review、整理 review 请求材料、明确 base/head 范围和 reviewer prompt。

当前 `code-quality.stage_assistant_candidates = []`。这不是辅助专家模型，也不是主/次技能模型。
```

Replace the sentence:

```markdown
同时补充了各主路由 skill 的 `SKILL.md` 边界说明：`code-reviewer` 不再自称主做安全扫描，`systematic-debugging` 明确只处理已经坏掉的问题，`tdd-guide` 明确接管测试先行开发，`requesting-code-review` 明确是阶段助手。
```

with:

```markdown
同时补充了各直接 route owner 的 `SKILL.md` 边界说明：`code-reviewer` 不再自称主做安全扫描，`systematic-debugging` 明确只处理已经坏掉的问题，`tdd-guide` 明确接管测试先行开发，`requesting-code-review` 明确接管 review request 准备。
```

- [ ] **Step 2: Create the second-pass governance note**

Create `docs/governance/code-quality-second-pass-consolidation-2026-04-30.md` with this structure:

````markdown
# code-quality 第二轮收敛记录

日期：2026-04-30

## 结论

`code-quality` 第二轮继续保持简化路由模型：

```text
candidate skill -> selected skill -> used / unused
```

本轮不恢复阶段助手、辅助专家、咨询态、主技能/次技能。当前 `stage_assistant_candidates = 0`。

## 当前直接 route owner

| skill | 负责的问题 |
|---|---|
| `code-reviewer` | 新鲜代码审查、PR review、质量和可维护性检查 |
| `requesting-code-review` | 准备发起代码审查，整理 review request |
| `receiving-code-review` | 收到 CodeRabbit/GitHub/人工评审意见后逐条判断和处理 |
| `security-reviewer` | 安全审计、OWASP、secret、auth、injection、权限风险 |
| `systematic-debugging` | bug、失败测试、构建失败、异常行为、根因定位 |
| `windows-hook-debugging` | Windows hook、Git Bash、WSL、cannot execute binary file |
| `tdd-guide` | TDD、先写失败测试、红绿重构 |
| `generating-test-reports` | 测试报告、coverage summary、JUnit/test summary |
| `verification-before-completion` | 收尾前确认测试、验收证据、完成声明前验证 |
| `deslop` | 清理 AI 生成代码废话注释、冗余防御式检查、模板噪声 |

## 旧目录处理

| skill | 处理 |
|---|---|
| `code-review` | 可复用 style guide 和 checker 已迁移到 `code-reviewer`，旧目录删除。 |
| `debugging-strategies` | 与 `systematic-debugging` 重叠，旧目录删除。 |
| `code-review-excellence` | 与 `code-reviewer` 重叠，旧目录删除。 |
| `error-resolver` | 资产重，保留目录；本轮不作为活跃直接路由 owner。 |

## 验证计划

实现完成后运行以下命令。最终验证输出在执行阶段更新到本记录。

```text
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
```

```text
.\scripts\verify\vibe-code-quality-pack-consolidation-audit-gate.ps1
```

```text
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

```text
.\scripts\verify\vibe-pack-regression-matrix.ps1
```

```text
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

```text
.\scripts\verify\vibe-offline-skills-gate.ps1
```

## 边界

本记录证明的是 routing/config/bundled skill cleanup，不证明这些 skills 已经在某个真实 Vibe 任务中被物质使用。
````

- [ ] **Step 3: Commit governance docs**

```powershell
git add docs/governance/code-quality-problem-first-consolidation-2026-04-27.md docs/governance/code-quality-second-pass-consolidation-2026-04-30.md
git commit -m "docs: record code quality second pass consolidation"
```

## Task 7: Refresh Lock Files And Generated Audit Artifacts

**Files:**
- Modify: `config/skills-lock.json`
- Optional generated: `outputs/skills-audit/code-quality-problem-map.json`
- Optional generated: `outputs/skills-audit/code-quality-problem-map.csv`
- Optional generated: `outputs/skills-audit/code-quality-problem-consolidation.md`

- [ ] **Step 1: Regenerate skills lock**

```powershell
.\scripts\verify\vibe-generate-skills-lock.ps1
```

Expected: command exits `0` and reports a `skills=` count that is lower by the number of physically deleted directories in this pass.

- [ ] **Step 2: Run the code-quality audit gate with artifacts**

```powershell
.\scripts\verify\vibe-code-quality-pack-consolidation-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
```

Expected: command exits `0` and prints:

```text
[PASS] vibe-code-quality-pack-consolidation-audit-gate passed
```

- [ ] **Step 3: Inspect generated problem map summary**

```powershell
Get-Content -Raw -LiteralPath outputs\skills-audit\code-quality-problem-map.json | ConvertFrom-Json | Select-Object -ExpandProperty summary | Format-List
```

Expected summary includes:

```text
target_route_authority_count : 10
target_stage_assistant_count : 0
```

- [ ] **Step 4: Commit lock and generated artifacts**

```powershell
git add config/skills-lock.json outputs/skills-audit/code-quality-problem-map.json outputs/skills-audit/code-quality-problem-map.csv outputs/skills-audit/code-quality-problem-consolidation.md
git commit -m "chore: refresh code quality skills lock and audit artifacts"
```

If `outputs/skills-audit` is intentionally ignored by git, commit only `config/skills-lock.json` and record the generated artifact paths in the final report.

## Task 8: Run Focused And Broad Verification

**Files:**
- No intended source edits.
- Verification may reveal stale references that require returning to Task 5.

- [ ] **Step 1: Run focused Python tests**

```powershell
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
```

Expected:

```text
passed
```

Record the exact passed count for the final report.

- [ ] **Step 2: Run skill-index routing audit**

```powershell
.\scripts\verify\vibe-skill-index-routing-audit.ps1
```

Expected:

```text
Failed: 0
Skill-index routing audit passed.
```

- [ ] **Step 3: Run pack regression matrix**

```powershell
.\scripts\verify\vibe-pack-regression-matrix.ps1
```

Expected:

```text
Failed: 0
Pack regression matrix checks passed.
```

- [ ] **Step 4: Run pack routing smoke**

```powershell
.\scripts\verify\vibe-pack-routing-smoke.ps1
```

Expected:

```text
Failed: 0
Pack routing smoke checks passed.
```

- [ ] **Step 5: Run offline skills gate**

```powershell
.\scripts\verify\vibe-offline-skills-gate.ps1
```

Expected:

```text
[PASS] offline skill closure gate passed.
```

- [ ] **Step 6: Run stale-reference search**

```powershell
rg -n -P "\b(code-review|debugging-strategies|code-review-excellence)\b" config scripts bundled
```

Expected: no live references to the deleted skill IDs. If matches remain only in explicit legacy alias whitelist files, record them and verify they do not require deleted skill directories.

- [ ] **Step 7: Run whitespace check**

```powershell
git diff --check
```

Expected: exit code `0` with no output.

- [ ] **Step 8: Update governance note with actual verification results**

In `docs/governance/code-quality-second-pass-consolidation-2026-04-30.md`, replace `## 验证计划` with `## 验证结果` and paste the exact command outputs from Steps 1-7. Use this structure for each command:

````markdown
### Focused Python tests

```text
python -m pytest tests/runtime_neutral/test_code_quality_pack_consolidation_audit.py tests/runtime_neutral/test_final_stage_assistant_removal.py -q
```
````

Paste the complete command output directly under the command line inside the same fenced block after each run. Repeat the same structure for `vibe-code-quality-pack-consolidation-audit-gate.ps1`, `vibe-skill-index-routing-audit.ps1`, `vibe-pack-regression-matrix.ps1`, `vibe-pack-routing-smoke.ps1`, `vibe-offline-skills-gate.ps1`, stale-reference search, and `git diff --check`.

- [ ] **Step 9: Commit verification-driven fixes if any**

If Steps 1-7 reveal stale references or narrow routing regressions, make the smallest fix, re-run the failing command, and commit:

```powershell
git status --short
git add config scripts bundled packages tests docs/governance
git commit -m "fix: stabilize code quality second pass verification"
```

If no fixes are needed, commit only the updated governance note:

```powershell
git add docs/governance/code-quality-second-pass-consolidation-2026-04-30.md
git commit -m "docs: add code quality verification evidence"
```

## Task 9: Final State Check

**Files:**
- No intended source edits.

- [ ] **Step 1: Confirm branch and worktree state**

```powershell
git status --short --branch
```

Expected:

```text
## main...origin/main [ahead N]
```

with no uncommitted file entries.

- [ ] **Step 2: Confirm latest commits**

```powershell
git log --oneline -8
```

Expected: the latest commits include the second-pass code-quality test, audit, migration/deletion, stale-reference cleanup, governance note, and lock/artifact commits.

- [ ] **Step 3: Prepare final report**

Final report must include:

```text
branch
latest commit hash
before/after counts
retained 10 direct route owners
stage_assistant_candidates = 0
deleted directories
retained error-resolver caveat
verification commands and exact pass/fail counts
stale-reference search result
statement that this proves routing/config/bundled cleanup, not material skill use in a real Vibe task
```
