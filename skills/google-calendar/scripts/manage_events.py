#!/usr/bin/env python3
"""Google Calendar 이벤트 관리 CLI.

일정 생성, 수정, 삭제를 위한 CLI 도구.

Usage:
    # 일정 생성 (시간 지정)
    uv run python manage_events.py create \
        --summary "팀 미팅" \
        --start "2026-01-06T14:00:00" \
        --end "2026-01-06T15:00:00" \
        --account work

    # 종일 일정 생성
    uv run python manage_events.py create \
        --summary "연차" \
        --start "2026-01-10" \
        --end "2026-01-11" \
        --account personal

    # 일정 수정
    uv run python manage_events.py update \
        --event-id "abc123" \
        --summary "팀 미팅 (변경)" \
        --account work

    # 일정 삭제
    uv run python manage_events.py delete \
        --event-id "abc123" \
        --account work

    # ADC 사용
    uv run python manage_events.py create \
        --summary "테스트" \
        --start "2026-01-06T10:00:00" \
        --end "2026-01-06T11:00:00" \
        --adc
"""

import argparse
import json
import sys
from pathlib import Path

from calendar_client import CalendarClient, ADCCalendarClient


def cmd_create(args):
    """일정 생성."""
    if args.adc:
        client = ADCCalendarClient()
    else:
        if not args.account:
            print("❌ --account 또는 --adc 필수", file=sys.stderr)
            sys.exit(1)
        base_path = Path(__file__).parent.parent
        client = CalendarClient(args.account, base_path)

    attendees = args.attendees.split(",") if args.attendees else None

    result = client.create_event(
        summary=args.summary,
        start=args.start,
        end=args.end,
        description=args.description,
        location=args.location,
        attendees=attendees,
        timezone=args.timezone,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 일정 생성 완료")
        print(f"   제목: {result['summary']}")
        print(f"   시간: {result['start']} ~ {result['end']}")
        print(f"   ID: {result['id']}")
        print(f"   링크: {result['html_link']}")


def cmd_update(args):
    """일정 수정."""
    if args.adc:
        client = ADCCalendarClient()
    else:
        if not args.account:
            print("❌ --account 또는 --adc 필수", file=sys.stderr)
            sys.exit(1)
        base_path = Path(__file__).parent.parent
        client = CalendarClient(args.account, base_path)

    result = client.update_event(
        event_id=args.event_id,
        summary=args.summary,
        start=args.start,
        end=args.end,
        description=args.description,
        location=args.location,
        timezone=args.timezone,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 일정 수정 완료")
        print(f"   제목: {result['summary']}")
        print(f"   시간: {result['start']} ~ {result['end']}")
        print(f"   ID: {result['id']}")
        print(f"   링크: {result['html_link']}")


def cmd_delete(args):
    """일정 삭제."""
    if args.adc:
        client = ADCCalendarClient()
    else:
        if not args.account:
            print("❌ --account 또는 --adc 필수", file=sys.stderr)
            sys.exit(1)
        base_path = Path(__file__).parent.parent
        client = CalendarClient(args.account, base_path)

    result = client.delete_event(event_id=args.event_id)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 일정 삭제 완료")
        print(f"   ID: {result['id']}")


def main():
    parser = argparse.ArgumentParser(description="Google Calendar 이벤트 관리")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 출력")

    subparsers = parser.add_subparsers(dest="command", help="명령")

    # create 명령
    create_parser = subparsers.add_parser("create", help="일정 생성")
    create_parser.add_argument("--summary", "-s", required=True, help="일정 제목")
    create_parser.add_argument("--start", required=True, help="시작 시간 (ISO format)")
    create_parser.add_argument("--end", required=True, help="종료 시간 (ISO format)")
    create_parser.add_argument("--description", "-d", help="설명")
    create_parser.add_argument("--location", "-l", help="장소")
    create_parser.add_argument("--attendees", help="참석자 (쉼표 구분)")
    create_parser.add_argument("--account", "-a", help="계정")
    create_parser.add_argument("--adc", action="store_true", help="ADC 사용")
    create_parser.add_argument("--timezone", default="Asia/Seoul", help="타임존")
    create_parser.add_argument("--json", "-j", action="store_true", help="JSON 출력")

    # update 명령
    update_parser = subparsers.add_parser("update", help="일정 수정")
    update_parser.add_argument("--event-id", required=True, help="이벤트 ID")
    update_parser.add_argument("--summary", "-s", help="새 제목")
    update_parser.add_argument("--start", help="새 시작 시간")
    update_parser.add_argument("--end", help="새 종료 시간")
    update_parser.add_argument("--description", "-d", help="새 설명")
    update_parser.add_argument("--location", "-l", help="새 장소")
    update_parser.add_argument("--account", "-a", help="계정")
    update_parser.add_argument("--adc", action="store_true", help="ADC 사용")
    update_parser.add_argument("--timezone", default="Asia/Seoul", help="타임존")
    update_parser.add_argument("--json", "-j", action="store_true", help="JSON 출력")

    # delete 명령
    delete_parser = subparsers.add_parser("delete", help="일정 삭제")
    delete_parser.add_argument("--event-id", required=True, help="이벤트 ID")
    delete_parser.add_argument("--account", "-a", help="계정")
    delete_parser.add_argument("--adc", action="store_true", help="ADC 사용")
    delete_parser.add_argument("--json", "-j", action="store_true", help="JSON 출력")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "create":
            cmd_create(args)
        elif args.command == "update":
            cmd_update(args)
        elif args.command == "delete":
            cmd_delete(args)
    except Exception as e:
        print(f"❌ 오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
