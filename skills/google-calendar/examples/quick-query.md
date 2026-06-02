# 빠른 조회 예시

## 오늘 일정

```bash
uv run python .claude/skills/google-calendar/scripts/fetch_events.py \
  --all --days 1 --pretty
```

## 이번 주 일정 (JSON)

```bash
uv run python .claude/skills/google-calendar/scripts/fetch_events.py \
  --all --days 7 --json
```

## 특정 계정만 조회

```bash
# 회사 캘린더만
uv run python .claude/skills/google-calendar/scripts/fetch_events.py \
  --account work --days 7 --pretty

# 개인 캘린더만
uv run python .claude/skills/google-calendar/scripts/fetch_events.py \
  --account personal --days 7 --pretty
```

## 캘린더 목록 확인

```bash
uv run python .claude/skills/google-calendar/scripts/fetch_events.py \
  --account work --list-calendars
```

## 프로그래밍 방식 사용

```python
from calendar_client import CalendarClient, fetch_all_events

# 단일 계정
client = CalendarClient("work")
events = client.get_events(days=7)

# 전체 계정 통합
result = fetch_all_events(days=7)
print(f"총 {result['total']}개 이벤트")
print(f"충돌: {len(result['conflicts'])}건")
```
