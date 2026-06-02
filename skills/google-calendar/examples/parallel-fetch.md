# 병렬 조회 예시

## Subagent 병렬 실행

여러 계정의 캘린더를 동시에 조회하려면 Task 도구를 병렬로 호출:

```
# 단일 메시지에 여러 Task 호출 (병렬 실행)

Task(
    subagent_type="general-purpose",
    prompt="다음 명령을 실행하고 결과를 JSON으로 반환:
    uv run python .claude/skills/google-calendar/scripts/fetch_events.py --account work --days 7 --json",
    model="haiku"
)

Task(
    subagent_type="general-purpose",
    prompt="다음 명령을 실행하고 결과를 JSON으로 반환:
    uv run python .claude/skills/google-calendar/scripts/fetch_events.py --account personal --days 7 --json",
    model="haiku"
)
```

## 결과 통합

각 subagent가 반환한 JSON을 파싱하여 통합:

```python
import json
from datetime import datetime

# subagent 결과들
work_events = json.loads(work_result)
personal_events = json.loads(personal_result)

# 통합 및 시간순 정렬
all_events = work_events + personal_events
all_events.sort(key=lambda x: x["start"])

# 날짜별 그룹화
events_by_date = {}
for event in all_events:
    date = event["start"].split("T")[0]
    events_by_date.setdefault(date, []).append(event)
```

## 충돌 감지

```python
def detect_conflicts(events):
    """동일 시간대 다른 계정 이벤트 = 충돌"""
    conflicts = []
    for i, e1 in enumerate(events):
        for e2 in events[i+1:]:
            if e1["account"] == e2["account"]:
                continue
            # 시간 겹침 확인
            if is_overlapping(e1, e2):
                conflicts.append((e1, e2))
    return conflicts
```

## 출력 예시

```
📅 2026-01-06 (월)

[09:00-10:00] 🔵 팀 스탠드업 (work)
[14:00-15:00] 🔵 고객 미팅 (work)
              ⚠️ 충돌: 개인 일정과 겹침
[14:00-14:30] 🟢 은행 방문 (personal)

📊 총 3개 일정 | 1건 충돌
```
