#!/usr/bin/env python3
"""Gmail 메시지 읽기 CLI.

Usage:
    # 메시지 읽기
    uv run python read_message.py --account work --id <message_id>

    # 스레드 전체 읽기
    uv run python read_message.py --account work --thread <thread_id>

    # 첨부파일 저장
    uv run python read_message.py --account work --id <message_id> --save-attachments ./downloads

    # JSON 출력
    uv run python read_message.py --account work --id <message_id> --json
"""

import argparse
import json
from pathlib import Path

from gmail_client import GmailClient, ADCGmailClient, get_all_accounts


def main():
    parser = argparse.ArgumentParser(description="Gmail 메시지 읽기")
    parser.add_argument("--account", "-a", help="계정 식별자")
    parser.add_argument("--adc", action="store_true", help="Application Default Credentials 사용")
    parser.add_argument("--id", "-i", help="메시지 ID")
    parser.add_argument("--thread", "-t", help="스레드 ID")
    parser.add_argument("--save-attachments", "-s", help="첨부파일 저장 경로")
    parser.add_argument("--json", action="store_true", help="JSON 형식 출력")

    args = parser.parse_args()
    base_path = Path(__file__).parent.parent

    if not args.id and not args.thread:
        parser.print_help()
        print()
        print("예시:")
        print("  uv run python read_message.py --account work --id abc123")
        print("  uv run python read_message.py --account work --thread xyz789")
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

    if args.thread:
        result = client.get_thread(args.thread)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"📧 스레드: {result['id']}")
            print(f"   메시지 수: {result['message_count']}")
            print("=" * 60)

            for msg in result["messages"]:
                print(f"\n📩 {msg['subject']}")
                print(f"   From: {msg['from']}")
                print(f"   To: {msg['to']}")
                print(f"   Date: {msg['date']}")
                print("-" * 60)
                print(msg['body'])
                print()
    else:
        result = client.get_message(args.id)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"📧 Subject: {result['subject']}")
            print(f"   From: {result['from']}")
            print(f"   To: {result['to']}")
            if result['cc']:
                print(f"   CC: {result['cc']}")
            print(f"   Date: {result['date']}")
            print(f"   Labels: {', '.join(result['label_ids'])}")

            if result['attachments']:
                print(f"\n📎 첨부파일:")
                for att in result['attachments']:
                    size_kb = att['size'] / 1024
                    print(f"   - {att['filename']} ({size_kb:.1f} KB)")

            print("\n" + "=" * 60)
            print(result['body'])

        if args.save_attachments and result.get('attachments'):
            save_path = Path(args.save_attachments)
            save_path.mkdir(parents=True, exist_ok=True)

            for att in result['attachments']:
                if att.get('attachment_id'):
                    data = client.get_attachment(args.id, att['attachment_id'])
                    filepath = save_path / att['filename']
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f"✅ 저장됨: {filepath}")


if __name__ == "__main__":
    main()
