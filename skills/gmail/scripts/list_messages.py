#!/usr/bin/env python3
"""Gmail 메시지 목록 조회 CLI.

Usage:
    # 받은편지함 최근 10개
    uv run python list_messages.py --account work --max 10

    # 검색 쿼리 사용
    uv run python list_messages.py --account work --query "from:user@example.com"
    uv run python list_messages.py --account work --query "is:unread"
    uv run python list_messages.py --account work --query "after:2024/01/01 before:2024/12/31"

    # 라벨로 필터
    uv run python list_messages.py --account work --labels INBOX,UNREAD

    # ADC 사용
    uv run python list_messages.py --adc --query "is:unread"
"""

import argparse
import json
from pathlib import Path

from gmail_client import GmailClient, ADCGmailClient, get_all_accounts


def format_message_summary(client: GmailClient, msg_id: str) -> dict:
    """메시지 요약 정보 조회."""
    msg = client.get_message(msg_id, format="metadata")
    return {
        "id": msg["id"],
        "from": msg["from"],
        "subject": msg["subject"],
        "date": msg["date"],
        "snippet": msg["snippet"][:100] + "..." if len(msg["snippet"]) > 100 else msg["snippet"],
        "labels": msg["label_ids"],
    }


def main():
    parser = argparse.ArgumentParser(description="Gmail 메시지 목록 조회")
    parser.add_argument("--account", "-a", help="계정 식별자")
    parser.add_argument("--adc", action="store_true", help="Application Default Credentials 사용")
    parser.add_argument("--query", "-q", default="", help="Gmail 검색 쿼리")
    parser.add_argument("--max", "-m", type=int, default=20, help="최대 결과 수")
    parser.add_argument("--labels", help="라벨 ID (쉼표 구분)")
    parser.add_argument("--include-spam-trash", action="store_true", help="스팸/휴지통 포함")
    parser.add_argument("--full", "-f", action="store_true", help="전체 메시지 정보 조회")
    parser.add_argument("--json", action="store_true", help="JSON 형식 출력")

    args = parser.parse_args()
    base_path = Path(__file__).parent.parent

    if args.adc:
        client = ADCGmailClient()
    else:
        accounts = get_all_accounts(base_path)
        if not accounts:
            print("❌ 등록된 계정이 없습니다.")
            print("   먼저 setup_auth.py --account <이름> 실행 필요")
            return

        account = args.account or accounts[0]
        client = GmailClient(account, base_path)

    label_ids = args.labels.split(",") if args.labels else None

    messages = client.list_messages(
        query=args.query,
        max_results=args.max,
        label_ids=label_ids,
        include_spam_trash=args.include_spam_trash,
    )

    if args.json:
        if args.full:
            result = [client.get_message(m["id"]) for m in messages]
        else:
            result = [format_message_summary(client, m["id"]) for m in messages]
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"📬 {len(messages)}개 메시지")
        print()
        for msg in messages:
            if args.full:
                full_msg = client.get_message(msg["id"])
                print(f"ID: {full_msg['id']}")
                print(f"From: {full_msg['from']}")
                print(f"To: {full_msg['to']}")
                print(f"Subject: {full_msg['subject']}")
                print(f"Date: {full_msg['date']}")
                print(f"Labels: {', '.join(full_msg['label_ids'])}")
                if full_msg['attachments']:
                    print(f"Attachments: {', '.join(a['filename'] for a in full_msg['attachments'])}")
                print("-" * 60)
                print(full_msg['body'][:500])
                if len(full_msg['body']) > 500:
                    print("... (truncated)")
                print("=" * 60)
                print()
            else:
                summary = format_message_summary(client, msg["id"])
                unread = "📩" if "UNREAD" in summary["labels"] else "📧"
                print(f"{unread} {summary['subject']}")
                print(f"   From: {summary['from']}")
                print(f"   Date: {summary['date']}")
                print(f"   {summary['snippet']}")
                print()


if __name__ == "__main__":
    main()
