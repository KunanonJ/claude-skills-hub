#!/usr/bin/env python3
"""Gmail 라벨 및 메시지 관리 CLI.

Usage:
    # 라벨 목록
    uv run python manage_labels.py --account work list-labels

    # 라벨 생성
    uv run python manage_labels.py --account work create-label --name "프로젝트/A"

    # 라벨 삭제
    uv run python manage_labels.py --account work delete-label --label-id Label_123

    # 읽음 표시
    uv run python manage_labels.py --account work mark-read --id <message_id>

    # 별표 추가
    uv run python manage_labels.py --account work star --id <message_id>

    # 보관처리
    uv run python manage_labels.py --account work archive --id <message_id>

    # 휴지통으로 이동
    uv run python manage_labels.py --account work trash --id <message_id>

    # 라벨 추가/제거
    uv run python manage_labels.py --account work modify --id <message_id> \
        --add-labels "Label_123,STARRED" --remove-labels "INBOX"

    # 초안 목록
    uv run python manage_labels.py --account work list-drafts

    # 초안 발송
    uv run python manage_labels.py --account work send-draft --draft-id <draft_id>

    # 프로필 조회
    uv run python manage_labels.py --account work profile
"""

import argparse
import json
from pathlib import Path

from gmail_client import GmailClient, ADCGmailClient, get_all_accounts


def main():
    parser = argparse.ArgumentParser(description="Gmail 라벨 및 메시지 관리")
    parser.add_argument("--account", "-a", help="계정 식별자")
    parser.add_argument("--adc", action="store_true", help="Application Default Credentials 사용")
    parser.add_argument("--json", action="store_true", help="JSON 형식 출력")

    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # 라벨 관리
    subparsers.add_parser("list-labels", help="라벨 목록")

    create_label = subparsers.add_parser("create-label", help="라벨 생성")
    create_label.add_argument("--name", required=True, help="라벨 이름")

    delete_label = subparsers.add_parser("delete-label", help="라벨 삭제")
    delete_label.add_argument("--label-id", required=True, help="라벨 ID")

    # 메시지 관리
    mark_read = subparsers.add_parser("mark-read", help="읽음 표시")
    mark_read.add_argument("--id", required=True, help="메시지 ID")

    mark_unread = subparsers.add_parser("mark-unread", help="읽지 않음 표시")
    mark_unread.add_argument("--id", required=True, help="메시지 ID")

    star = subparsers.add_parser("star", help="별표 추가")
    star.add_argument("--id", required=True, help="메시지 ID")

    unstar = subparsers.add_parser("unstar", help="별표 제거")
    unstar.add_argument("--id", required=True, help="메시지 ID")

    archive = subparsers.add_parser("archive", help="보관처리")
    archive.add_argument("--id", required=True, help="메시지 ID")

    trash = subparsers.add_parser("trash", help="휴지통으로 이동")
    trash.add_argument("--id", required=True, help="메시지 ID")

    untrash = subparsers.add_parser("untrash", help="휴지통에서 복원")
    untrash.add_argument("--id", required=True, help="메시지 ID")

    modify = subparsers.add_parser("modify", help="라벨 수정")
    modify.add_argument("--id", required=True, help="메시지 ID")
    modify.add_argument("--add-labels", help="추가할 라벨 (쉼표 구분)")
    modify.add_argument("--remove-labels", help="제거할 라벨 (쉼표 구분)")

    # 초안 관리
    subparsers.add_parser("list-drafts", help="초안 목록")

    send_draft = subparsers.add_parser("send-draft", help="초안 발송")
    send_draft.add_argument("--draft-id", required=True, help="초안 ID")

    delete_draft = subparsers.add_parser("delete-draft", help="초안 삭제")
    delete_draft.add_argument("--draft-id", required=True, help="초안 ID")

    # 프로필
    subparsers.add_parser("profile", help="프로필 조회")

    args = parser.parse_args()
    base_path = Path(__file__).parent.parent

    if not args.command:
        parser.print_help()
        return

    if args.adc:
        client = ADCGmailClient()
    else:
        accounts = get_all_accounts(base_path)
        if not accounts:
            print("❌ 등록된 계정이 없습니다.")
            return

        account = args.account or accounts[0]
        client = GmailClient(account, base_path)

    result = None

    # 라벨 명령어
    if args.command == "list-labels":
        result = client.list_labels()
        if not args.json:
            print("🏷️  라벨 목록:")
            for label in result:
                label_type = "📁" if label["type"] == "system" else "🏷️"
                print(f"  {label_type} {label['name']} ({label['id']})")
            return

    elif args.command == "create-label":
        result = client.create_label(args.name)
        if not args.json:
            print(f"✅ 라벨 생성됨: {result['name']} ({result['id']})")
            return

    elif args.command == "delete-label":
        result = client.delete_label(args.label_id)
        if not args.json:
            print(f"✅ 라벨 삭제됨: {args.label_id}")
            return

    # 메시지 명령어
    elif args.command == "mark-read":
        result = client.mark_as_read(args.id)
    elif args.command == "mark-unread":
        result = client.mark_as_unread(args.id)
    elif args.command == "star":
        result = client.star_message(args.id)
    elif args.command == "unstar":
        result = client.unstar_message(args.id)
    elif args.command == "archive":
        result = client.archive_message(args.id)
    elif args.command == "trash":
        result = client.trash_message(args.id)
    elif args.command == "untrash":
        result = client.untrash_message(args.id)
    elif args.command == "modify":
        add_labels = args.add_labels.split(",") if args.add_labels else None
        remove_labels = args.remove_labels.split(",") if args.remove_labels else None
        result = client.modify_message(args.id, add_labels, remove_labels)

    # 초안 명령어
    elif args.command == "list-drafts":
        drafts = client.list_drafts()
        if not args.json:
            print(f"📝 초안 {len(drafts)}개")
            for draft in drafts:
                detail = client.get_draft(draft["id"])
                msg = detail["message"]
                print(f"  - {msg['subject']} → {msg['to']}")
                print(f"    ID: {draft['id']}")
            return
        result = drafts

    elif args.command == "send-draft":
        result = client.send_draft(args.draft_id)
        if not args.json:
            print(f"✅ 초안 발송됨: {result['id']}")
            return

    elif args.command == "delete-draft":
        result = client.delete_draft(args.draft_id)
        if not args.json:
            print(f"✅ 초안 삭제됨: {args.draft_id}")
            return

    # 프로필
    elif args.command == "profile":
        result = client.get_profile()
        if not args.json:
            print(f"📧 {result['email']}")
            print(f"   메시지: {result['messages_total']:,}개")
            print(f"   스레드: {result['threads_total']:,}개")
            return

    if args.json and result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result:
        print(f"✅ {args.command} 완료")
        print(f"   ID: {result.get('id')}")


if __name__ == "__main__":
    main()
