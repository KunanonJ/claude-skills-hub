---
name: history-insight
description: |
  Claude Code 세션 히스토리 분석 스킬. 트리거:
  - "세션 분석해줘", "패턴 분석해줘", "반복 패턴 찾아줘"
  - "최근 일주일 세션 분석", "세션 히스토리 캡처"
  - "자동화할 패턴 찾아줘", "스킬로 만들 패턴"
  - "what we discussed", "session history"
version: 1.2.0
user-invocable: true
---

# History Insight

Claude Code 세션 히스토리를 분석하고 인사이트/반복 패턴을 추출합니다.

---

## 분석 모드

| 모드 | 트리거 | 목적 |
|------|--------|------|
| **일반 인사이트** | "세션 캡처", "세션 요약" | 세션 내용 요약 및 인사이트 추출 |
| **패턴 분석** | "패턴 분석", "반복 패턴", "자동화 패턴" | 반복되는 프롬프트/작업 감지 → 자동화 제안 |

**모드 선택:**
- 명시된 경우: 해당 모드로 진행
- 명시되지 않은 경우: AskUserQuestion으로 선택

---

## Data Location

```
~/.claude/projects/<encoded-cwd>/*.jsonl
```

**Path Encoding:** `/Users/foo/project` → `-Users-foo-project`

> 상세 파일 포맷: `${baseDir}/references/session-file-format.md`

---

## Execution Algorithm

### Step 1: Ask Scope [MANDATORY]

**스코프 결정:**

1. **명시된 경우** (AskUserQuestion 생략 가능):
   - "현재 프로젝트만" / "이 프로젝트" → `current_project`
   - "모든 세션" / "전체" → `all_sessions`

2. **명시되지 않은 경우** - AskUserQuestion 호출:
   ```
   question: "세션 검색 범위를 선택하세요"
   options:
     - "현재 프로젝트만" → ~/.claude/projects/<encoded-cwd>/*.jsonl
     - "모든 Claude Code 세션" → ~/.claude/projects/**/*.jsonl
   ```

---

### Step 2: Find Session Files

```bash
# Current project only
find ~/.claude/projects/<encoded-cwd> -name "*.jsonl" -type f

# All sessions (모든 프로젝트)
find ~/.claude/projects -name "*.jsonl" -type f
```

**날짜 필터링**: 파일의 mtime(수정시간) 확인 후 필터. OS별 `stat` 옵션 다름:
- macOS: `stat -f "%Sm" -t "%Y-%m-%d" <file>`
- Linux: `stat -c "%y" <file>`

---

### Step 3: Process Sessions

#### Decision Tree

```
Session files found?
├─ No → Error: "No sessions found"
└─ Yes → How many files?
    ├─ 1-3 files → Direct Read + parse
    └─ 4+ files → Batch Extract Pipeline
```

#### 1-3 Files

직접 Read로 JSONL 파싱. 파일이 크면(≥5000 tokens) `extract-session.sh` 사용:
```bash
${baseDir}/scripts/extract-session.sh <session.jsonl>
```

#### 4+ Files: Batch Extract Pipeline

1. 캐시 디렉토리 생성 (`/tmp/cc-cache/<analysis-name>/`)
2. 세션 목록 저장 (`sessions.txt`)
3. jq로 메시지 일괄 추출 (`user_messages.txt`)
4. 정리 및 필터링 (`clean_messages.txt`)
5. Task(opus)로 종합 분석

#### 파일이 너무 클 때: 병렬 배치 분석

`clean_messages.txt`가 너무 커서 Read 실패 시:

1. **파일 분할**:
   ```bash
   split -l 2000 clean_messages.txt /tmp/cc-cache/<name>/batch_
   ```

2. **병렬 Task(opus) 호출**:
   ```
   Task(subagent_type="general-purpose", model="opus", run_in_background=true)
   prompt: "batch_XX 파일을 읽고 주제/패턴 요약해줘"
   ```

3. **결과 병합**: Task(opus)로 종합

---

### Step 4: Report Results (일반 인사이트 모드)

```markdown
## Session Capture Complete

- **Sessions:** N files processed
- **Messages:** X total, Y after filter

### Extracted Insights
[분석 결과]
```

---

## 패턴 분석 모드

패턴 분석 모드가 선택된 경우, Step 3 이후 아래 알고리즘 실행:

### Pattern Step 1: 날짜 범위 설정

```
기본값: 최근 7일
옵션: --days N (사용자 지정)
```

**날짜 필터링:**
```bash
# macOS: 최근 7일 파일만
find ~/.claude/projects/<encoded-cwd> -name "*.jsonl" -type f -mtime -7
```

### Pattern Step 2: 사용자 메시지 추출

```bash
# 모든 세션에서 user 메시지만 추출
for f in *.jsonl; do
  jq -r 'select(.type == "user") | .message.content' "$f"
done > all_user_messages.txt
```

### Pattern Step 3: 반복 패턴 감지

**감지 대상:**
1. **반복 프롬프트**: 유사한 요청이 3회 이상 등장
2. **반복 명령어**: 같은 Bash 명령 패턴 (git, npm, etc.)
3. **반복 워크플로우**: 동일한 작업 순서 (예: 파일 읽기 → 수정 → 커밋)
4. **반복 질문**: 비슷한 질문 패턴

**분석 방법:**
```
Task(subagent_type="general-purpose", model="opus")
prompt: |
  아래 사용자 메시지들에서 반복되는 패턴을 찾아주세요.

  분석 기준:
  1. 3회 이상 유사하게 등장하는 요청
  2. 동일한 작업 흐름 (순서가 같은 작업들)
  3. 비슷한 질문/명령 패턴

  각 패턴에 대해:
  - 패턴 설명
  - 등장 빈도
  - 예시 메시지 (2-3개)
  - 자동화 가능성 (높음/중간/낮음)
```

### Pattern Step 4: 자동화 제안 생성

발견된 패턴에 대해 자동화 유형 제안:

| 패턴 특성 | 권장 자동화 |
|----------|------------|
| 단순 반복 프롬프트 | **Command** (`.claude/commands/`) |
| 복잡한 워크플로우 | **Skill** (`.claude/skills/`) |
| 독립적 분석/처리 | **Agent** (`.claude/agents/`) |
| 이벤트 기반 자동 실행 | **Hook** (`settings.local.json`) |

**제안 생성:**
```
Task(subagent_type="general-purpose")
prompt: |
  .claude/agents/session-wrap/automation-scout.md 지침을 참고하여
  발견된 패턴들에 대해 구체적인 자동화 제안을 생성하세요.

  각 제안 포함사항:
  - 자동화 유형 (command/skill/agent/hook)
  - 트리거 (어떻게 실행될지)
  - 구현 개요
  - 예상 효과
```

### Pattern Step 5: 패턴 분석 결과 출력

```markdown
## 패턴 분석 결과

- **분석 기간**: YYYY-MM-DD ~ YYYY-MM-DD (N일)
- **분석 세션**: N개
- **총 메시지**: X개

---

### 발견된 패턴 (빈도순)

#### 1. [패턴명]
- **빈도**: N회
- **유형**: 반복 프롬프트 / 반복 워크플로우 / 반복 명령
- **예시**:
  - "..."
  - "..."
- **자동화 가능성**: 높음 / 중간 / 낮음

---

### 자동화 제안

#### 1. [제안명]
- **유형**: command / skill / agent / hook
- **트리거**: [어떻게 실행될지]
- **구현 개요**:
  ```
  [핵심 로직]
  ```
- **예상 효과**: [시간 절약, 일관성 확보 등]

---

### 요약
- **자동화 권장 패턴**: N개
- **즉시 구현 가능**: M개
- **추가 검토 필요**: K개
```

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No session files found | "No session files found for this project." |
| File too large | Auto-preprocess with extract-session.sh |
| jq not installed | "Error: jq is required. Install with: brew install jq" |
| Task failed | "Warning: Could not process [file]. Skipping." |
| 0 relevant sessions | "No sessions matched your criteria." |

---

## Security Notes

- 출력에 전체 경로 노출 금지 (`~` prefix 사용)

---

## Related Resources

- **`${baseDir}/scripts/extract-session.sh`** - JSONL 압축 (thinking, tool_use 제거)
- **`${baseDir}/references/session-file-format.md`** - JSONL 구조 및 파싱
