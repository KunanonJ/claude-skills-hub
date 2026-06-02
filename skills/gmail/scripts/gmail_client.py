"""Gmail API 클라이언트.

여러 Google 계정의 Gmail을 조회/발송하기 위한 클라이언트.
저장된 refresh token을 사용하여 매번 인증 없이 API 호출.

Features:
    - 다중 계정 지원 (work, personal 등)
    - Rate Limiting & Quota Management (P0)
    - Exponential Backoff for Error Handling (P0)
    - Batch Processing for Bulk Operations (P1)
    - Local Caching for API Optimization (P1)

Environment Variables:
    GMAIL_SKILL_PATH: Skill 루트 경로 (기본값: 이 파일의 부모의 부모)
    GMAIL_TIMEOUT: API 요청 타임아웃 초 (기본값: 30)
    GMAIL_CACHE_DIR: 캐시 디렉토리 (기본값: .cache/gmail)
    GMAIL_ENABLE_CACHE: 캐시 활성화 여부 (기본값: true)
    GMAIL_ENABLE_QUOTA: 할당량 관리 활성화 여부 (기본값: true)
"""

import base64
import json
import logging
import mimetypes
import os
from datetime import datetime
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Core modules for enhanced functionality
try:
    from .core import (
        QuotaManager,
        QuotaUnit,
        exponential_backoff,
        RetryConfig,
        EmailCache,
        BatchProcessor,
    )
except ImportError:
    # Fallback for direct script execution
    from core import (
        QuotaManager,
        QuotaUnit,
        exponential_backoff,
        RetryConfig,
        EmailCache,
        BatchProcessor,
    )

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = int(os.environ.get("GMAIL_TIMEOUT", "30"))
ENABLE_CACHE = os.environ.get("GMAIL_ENABLE_CACHE", "true").lower() == "true"
ENABLE_QUOTA = os.environ.get("GMAIL_ENABLE_QUOTA", "true").lower() == "true"


class GmailClient:
    """단일 Google 계정의 Gmail 클라이언트.

    Enhanced with:
        - Rate limiting & quota management
        - Exponential backoff for error handling
        - Local caching for API optimization
        - Batch processing support
    """

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.modify",  # 읽기/수정/삭제
        "https://www.googleapis.com/auth/gmail.send",    # 메일 발송
        "https://www.googleapis.com/auth/gmail.labels",  # 라벨 관리
    ]

    def __init__(
        self,
        account_name: str,
        base_path: Optional[Path] = None,
        timeout: int = DEFAULT_TIMEOUT,
        enable_cache: bool = ENABLE_CACHE,
        enable_quota: bool = ENABLE_QUOTA,
    ):
        """
        Args:
            account_name: 계정 식별자 (예: 'work', 'personal')
            base_path: skill 루트 경로
            timeout: API 요청 타임아웃 (초)
            enable_cache: 캐시 활성화 여부
            enable_quota: 할당량 관리 활성화 여부
        """
        self.account_name = account_name
        self.timeout = timeout
        self.enable_cache = enable_cache
        self.enable_quota = enable_quota

        if base_path:
            self.base_path = base_path
        elif os.environ.get("GMAIL_SKILL_PATH"):
            self.base_path = Path(os.environ["GMAIL_SKILL_PATH"])
        else:
            self.base_path = Path(__file__).parent.parent

        self.creds = self._load_credentials()
        self._service = None

        # Initialize core components
        self._cache: Optional[EmailCache] = None
        self._quota_manager: Optional[QuotaManager] = None
        self._batch_processor: Optional[BatchProcessor] = None

        if enable_cache:
            cache_dir = os.environ.get("GMAIL_CACHE_DIR") or str(
                self.base_path / ".cache" / "gmail"
            )
            self._cache = EmailCache(cache_dir=cache_dir)

        if enable_quota:
            self._quota_manager = QuotaManager()

    @property
    def service(self):
        """Lazy-load Gmail service."""
        if self._service is None:
            self._service = build("gmail", "v1", credentials=self.creds)
        return self._service

    @property
    def cache(self) -> Optional[EmailCache]:
        """Get cache manager instance."""
        return self._cache

    @property
    def quota_manager(self) -> Optional[QuotaManager]:
        """Get quota manager instance."""
        return self._quota_manager

    @property
    def batch_processor(self) -> BatchProcessor:
        """Get batch processor instance (lazy-loaded)."""
        if self._batch_processor is None:
            self._batch_processor = BatchProcessor(
                service=self.service,
                quota_manager=self._quota_manager,
                user=self.account_name,
            )
        return self._batch_processor

    def _record_quota(self, units: int) -> None:
        """Record quota usage if quota management is enabled."""
        if self._quota_manager:
            self._quota_manager.record_usage(self.account_name, units)

    def _wait_for_quota(self, units: int) -> None:
        """Wait for quota availability if quota management is enabled."""
        if self._quota_manager:
            self._quota_manager.wait_for_quota(self.account_name, units)

    def _load_credentials(self):
        """저장된 refresh token으로 credentials 로드 및 갱신."""
        token_path = self.base_path / f"accounts/{self.account_name}.json"

        if not token_path.exists():
            raise FileNotFoundError(
                f"계정 '{self.account_name}'의 토큰이 없습니다. "
                f"먼저 setup_auth.py --account {self.account_name} 실행 필요"
            )

        with open(token_path) as f:
            token_data = json.load(f)

        if "client_id" in token_data and "type" not in token_data:
            creds = Credentials(
                token=token_data.get("token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=token_data.get("client_id"),
                client_secret=token_data.get("client_secret"),
                scopes=self.SCOPES,
            )
            quota_project = token_data.get("quota_project_id", "teamattention")
            creds = creds.with_quota_project(quota_project)
        else:
            creds = Credentials.from_authorized_user_info(token_data, self.SCOPES)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as f:
                json.dump(json.loads(creds.to_json()), f, indent=2)

        return creds

    # =========================================================================
    # Messages
    # =========================================================================

    def list_messages(
        self,
        query: str = "",
        max_results: int = 20,
        label_ids: Optional[list[str]] = None,
        include_spam_trash: bool = False,
        use_cache: bool = True,
    ) -> list[dict]:
        """메시지 목록 조회.

        Args:
            query: Gmail 검색 쿼리 (예: "from:user@example.com", "is:unread")
            max_results: 최대 결과 수
            label_ids: 필터할 라벨 ID 목록
            include_spam_trash: 스팸/휴지통 포함 여부
            use_cache: 캐시 사용 여부 (기본값: True)

        Returns:
            메시지 목록 (id, threadId 포함)
        """
        # Check cache first
        if use_cache and self._cache:
            cached = self._cache.get_list(self.account_name, query, label_ids)
            if cached is not None:
                logger.debug(f"Cache hit for list query: {query}")
                return cached[:max_results]

        messages = []
        page_token = None

        @exponential_backoff(max_retries=5)
        def _list_page(**kwargs):
            return self.service.users().messages().list(**kwargs).execute()

        while len(messages) < max_results:
            kwargs = {
                "userId": "me",
                "maxResults": min(max_results - len(messages), 100),
                "includeSpamTrash": include_spam_trash,
            }
            if query:
                kwargs["q"] = query
            if label_ids:
                kwargs["labelIds"] = label_ids
            if page_token:
                kwargs["pageToken"] = page_token

            # Wait for quota before API call
            self._wait_for_quota(QuotaUnit.MESSAGES_LIST)

            result = _list_page(**kwargs)

            # Record quota usage
            self._record_quota(QuotaUnit.MESSAGES_LIST)

            for msg in result.get("messages", []):
                messages.append(msg)

            page_token = result.get("nextPageToken")
            if not page_token:
                break

        # Cache the results
        if use_cache and self._cache and messages:
            self._cache.set_list(self.account_name, query, messages, label_ids)

        return messages

    def get_message(
        self,
        message_id: str,
        format: str = "full",
        use_cache: bool = True,
    ) -> dict:
        """메시지 상세 조회.

        Args:
            message_id: 메시지 ID
            format: 응답 형식 (minimal, full, raw, metadata)
            use_cache: 캐시 사용 여부 (기본값: True)

        Returns:
            메시지 상세 정보
        """
        # Check cache first (only for full/metadata formats)
        if use_cache and self._cache and format in ("full", "metadata"):
            cached = self._cache.get_message(
                self.account_name,
                message_id,
                metadata_only=(format == "metadata"),
            )
            if cached is not None:
                logger.debug(f"Cache hit for message: {message_id}")
                return cached

        @exponential_backoff(max_retries=5)
        def _get_message():
            return (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format=format)
                .execute()
            )

        # Wait for quota before API call
        self._wait_for_quota(QuotaUnit.MESSAGES_GET)

        result = _get_message()

        # Record quota usage
        self._record_quota(QuotaUnit.MESSAGES_GET)

        parsed = self._parse_message(result)

        # Cache the result
        if use_cache and self._cache and format in ("full", "metadata"):
            self._cache.set_message(self.account_name, message_id, parsed)

        return parsed

    def _parse_message(self, msg: dict) -> dict:
        """API 응답을 파싱하여 읽기 쉬운 형식으로 변환."""
        headers = {}
        for header in msg.get("payload", {}).get("headers", []):
            name = header["name"].lower()
            if name in ("from", "to", "cc", "bcc", "subject", "date", "message-id"):
                headers[name] = header["value"]

        body = ""
        attachments = []

        payload = msg.get("payload", {})
        body, attachments = self._extract_body_and_attachments(payload, msg["id"])

        return {
            "id": msg["id"],
            "thread_id": msg["threadId"],
            "label_ids": msg.get("labelIds", []),
            "snippet": msg.get("snippet", ""),
            "from": headers.get("from", ""),
            "to": headers.get("to", ""),
            "cc": headers.get("cc", ""),
            "subject": headers.get("subject", "(제목 없음)"),
            "date": headers.get("date", ""),
            "message_id": headers.get("message-id", ""),
            "body": body,
            "attachments": attachments,
            "size_estimate": msg.get("sizeEstimate", 0),
            "internal_date": msg.get("internalDate", ""),
        }

    def _extract_body_and_attachments(
        self, payload: dict, message_id: str
    ) -> tuple[str, list[dict]]:
        """메시지 본문과 첨부파일 추출."""
        body = ""
        attachments = []

        mime_type = payload.get("mimeType", "")

        if mime_type.startswith("multipart/"):
            for part in payload.get("parts", []):
                part_body, part_attachments = self._extract_body_and_attachments(
                    part, message_id
                )
                if part_body:
                    body = part_body
                attachments.extend(part_attachments)
        else:
            if payload.get("filename"):
                attachments.append(
                    {
                        "filename": payload["filename"],
                        "mime_type": mime_type,
                        "size": payload.get("body", {}).get("size", 0),
                        "attachment_id": payload.get("body", {}).get("attachmentId"),
                    }
                )
            elif mime_type in ("text/plain", "text/html"):
                data = payload.get("body", {}).get("data", "")
                if data:
                    decoded = base64.urlsafe_b64decode(data).decode("utf-8")
                    if mime_type == "text/plain" or not body:
                        body = decoded

        return body, attachments

    def get_attachment(self, message_id: str, attachment_id: str) -> bytes:
        """첨부파일 다운로드.

        Args:
            message_id: 메시지 ID
            attachment_id: 첨부파일 ID

        Returns:
            첨부파일 바이너리 데이터
        """
        result = (
            self.service.users()
            .messages()
            .attachments()
            .get(userId="me", messageId=message_id, id=attachment_id)
            .execute()
        )
        return base64.urlsafe_b64decode(result["data"])

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        html: bool = False,
        attachments: Optional[list[str]] = None,
        reply_to_message_id: Optional[str] = None,
        thread_id: Optional[str] = None,
    ) -> dict:
        """메일 발송.

        Args:
            to: 수신자 (쉼표로 구분 가능)
            subject: 제목
            body: 본문
            cc: 참조
            bcc: 숨은 참조
            html: HTML 형식 여부
            attachments: 첨부파일 경로 목록
            reply_to_message_id: 답장할 메시지 ID (In-Reply-To 헤더용)
            thread_id: 스레드 ID (답장 시)

        Returns:
            발송된 메시지 정보
        """
        if attachments:
            message = MIMEMultipart()
            message.attach(MIMEText(body, "html" if html else "plain", "utf-8"))
            for filepath in attachments:
                self._attach_file(message, filepath)
        else:
            message = MIMEText(body, "html" if html else "plain", "utf-8")

        message["to"] = to
        message["subject"] = subject
        if cc:
            message["cc"] = cc
        if bcc:
            message["bcc"] = bcc
        if reply_to_message_id:
            message["In-Reply-To"] = reply_to_message_id
            message["References"] = reply_to_message_id

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        body_data = {"raw": raw}
        if thread_id:
            body_data["threadId"] = thread_id

        @exponential_backoff(max_retries=5)
        def _send():
            return (
                self.service.users().messages().send(userId="me", body=body_data).execute()
            )

        # Wait for quota before API call (send uses 100 units)
        self._wait_for_quota(QuotaUnit.MESSAGES_SEND)

        result = _send()

        # Record quota usage
        self._record_quota(QuotaUnit.MESSAGES_SEND)

        # Invalidate list cache after sending
        if self._cache:
            self._cache.invalidate_lists(self.account_name)

        return {
            "id": result["id"],
            "thread_id": result["threadId"],
            "label_ids": result.get("labelIds", []),
            "status": "sent",
        }

    def _attach_file(self, message: MIMEMultipart, filepath: str) -> None:
        """파일을 메시지에 첨부."""
        path = Path(filepath)
        content_type, encoding = mimetypes.guess_type(str(path))

        if content_type is None:
            content_type = "application/octet-stream"

        main_type, sub_type = content_type.split("/", 1)

        with open(path, "rb") as f:
            data = f.read()

        if main_type == "text":
            attachment = MIMEText(data.decode("utf-8"), _subtype=sub_type)
        elif main_type == "image":
            attachment = MIMEImage(data, _subtype=sub_type)
        elif main_type == "audio":
            attachment = MIMEAudio(data, _subtype=sub_type)
        else:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(data)
            encoders.encode_base64(attachment)

        attachment.add_header(
            "Content-Disposition", "attachment", filename=path.name
        )
        message.attach(attachment)

    def modify_message(
        self,
        message_id: str,
        add_label_ids: Optional[list[str]] = None,
        remove_label_ids: Optional[list[str]] = None,
    ) -> dict:
        """메시지 라벨 수정.

        Args:
            message_id: 메시지 ID
            add_label_ids: 추가할 라벨 ID
            remove_label_ids: 제거할 라벨 ID

        Returns:
            수정된 메시지 정보
        """
        body = {}
        if add_label_ids:
            body["addLabelIds"] = add_label_ids
        if remove_label_ids:
            body["removeLabelIds"] = remove_label_ids

        @exponential_backoff(max_retries=5)
        def _modify():
            return (
                self.service.users()
                .messages()
                .modify(userId="me", id=message_id, body=body)
                .execute()
            )

        # Wait for quota before API call
        self._wait_for_quota(QuotaUnit.MESSAGES_MODIFY)

        result = _modify()

        # Record quota usage
        self._record_quota(QuotaUnit.MESSAGES_MODIFY)

        # Invalidate cache for this message
        if self._cache:
            self._cache.invalidate_message(self.account_name, message_id)

        return {
            "id": result["id"],
            "thread_id": result["threadId"],
            "label_ids": result.get("labelIds", []),
            "status": "modified",
        }

    def mark_as_read(self, message_id: str) -> dict:
        """읽음으로 표시."""
        return self.modify_message(message_id, remove_label_ids=["UNREAD"])

    def mark_as_unread(self, message_id: str) -> dict:
        """읽지 않음으로 표시."""
        return self.modify_message(message_id, add_label_ids=["UNREAD"])

    def star_message(self, message_id: str) -> dict:
        """별표 추가."""
        return self.modify_message(message_id, add_label_ids=["STARRED"])

    def unstar_message(self, message_id: str) -> dict:
        """별표 제거."""
        return self.modify_message(message_id, remove_label_ids=["STARRED"])

    def archive_message(self, message_id: str) -> dict:
        """보관처리 (INBOX 라벨 제거)."""
        return self.modify_message(message_id, remove_label_ids=["INBOX"])

    def trash_message(self, message_id: str) -> dict:
        """휴지통으로 이동."""
        @exponential_backoff(max_retries=5)
        def _trash():
            return (
                self.service.users()
                .messages()
                .trash(userId="me", id=message_id)
                .execute()
            )

        self._wait_for_quota(QuotaUnit.MESSAGES_TRASH)
        result = _trash()
        self._record_quota(QuotaUnit.MESSAGES_TRASH)

        # Invalidate cache
        if self._cache:
            self._cache.invalidate_message(self.account_name, message_id)
            self._cache.invalidate_lists(self.account_name)

        return {
            "id": result["id"],
            "status": "trashed",
        }

    def untrash_message(self, message_id: str) -> dict:
        """휴지통에서 복원."""
        @exponential_backoff(max_retries=5)
        def _untrash():
            return (
                self.service.users()
                .messages()
                .untrash(userId="me", id=message_id)
                .execute()
            )

        self._wait_for_quota(QuotaUnit.MESSAGES_UNTRASH)
        result = _untrash()
        self._record_quota(QuotaUnit.MESSAGES_UNTRASH)

        # Invalidate cache
        if self._cache:
            self._cache.invalidate_message(self.account_name, message_id)
            self._cache.invalidate_lists(self.account_name)

        return {
            "id": result["id"],
            "status": "untrashed",
        }

    def delete_message(self, message_id: str) -> dict:
        """메시지 영구 삭제 (복구 불가)."""
        @exponential_backoff(max_retries=5)
        def _delete():
            self.service.users().messages().delete(userId="me", id=message_id).execute()

        self._wait_for_quota(QuotaUnit.MESSAGES_DELETE)
        _delete()
        self._record_quota(QuotaUnit.MESSAGES_DELETE)

        # Invalidate cache
        if self._cache:
            self._cache.invalidate_message(self.account_name, message_id)
            self._cache.invalidate_lists(self.account_name)

        return {
            "id": message_id,
            "status": "deleted",
        }

    # =========================================================================
    # Threads
    # =========================================================================

    def list_threads(
        self,
        query: str = "",
        max_results: int = 20,
        label_ids: Optional[list[str]] = None,
    ) -> list[dict]:
        """스레드 목록 조회."""
        threads = []
        page_token = None

        while len(threads) < max_results:
            kwargs = {
                "userId": "me",
                "maxResults": min(max_results - len(threads), 100),
            }
            if query:
                kwargs["q"] = query
            if label_ids:
                kwargs["labelIds"] = label_ids
            if page_token:
                kwargs["pageToken"] = page_token

            result = self.service.users().threads().list(**kwargs).execute()

            for thread in result.get("threads", []):
                threads.append(thread)

            page_token = result.get("nextPageToken")
            if not page_token:
                break

        return threads

    def get_thread(self, thread_id: str, format: str = "full") -> dict:
        """스레드 상세 조회."""
        result = (
            self.service.users()
            .threads()
            .get(userId="me", id=thread_id, format=format)
            .execute()
        )

        messages = [self._parse_message(msg) for msg in result.get("messages", [])]

        return {
            "id": result["id"],
            "messages": messages,
            "message_count": len(messages),
        }

    def trash_thread(self, thread_id: str) -> dict:
        """스레드 휴지통으로 이동."""
        result = (
            self.service.users()
            .threads()
            .trash(userId="me", id=thread_id)
            .execute()
        )
        return {
            "id": result["id"],
            "status": "trashed",
        }

    # =========================================================================
    # Labels
    # =========================================================================

    def list_labels(self, use_cache: bool = True) -> list[dict]:
        """라벨 목록 조회.

        Args:
            use_cache: 캐시 사용 여부 (기본값: True)

        Returns:
            라벨 목록
        """
        # Check cache first
        if use_cache and self._cache:
            cached = self._cache.get_labels(self.account_name)
            if cached is not None:
                logger.debug("Cache hit for labels")
                return cached

        @exponential_backoff(max_retries=5)
        def _list_labels():
            return self.service.users().labels().list(userId="me").execute()

        self._wait_for_quota(QuotaUnit.LABELS_LIST)
        result = _list_labels()
        self._record_quota(QuotaUnit.LABELS_LIST)

        labels = []
        for label in result.get("labels", []):
            labels.append(
                {
                    "id": label["id"],
                    "name": label["name"],
                    "type": label.get("type", "user"),
                    "message_list_visibility": label.get("messageListVisibility"),
                    "label_list_visibility": label.get("labelListVisibility"),
                }
            )

        # Cache the results
        if use_cache and self._cache:
            self._cache.set_labels(self.account_name, labels)

        return labels

    def get_label(self, label_id: str) -> dict:
        """라벨 상세 조회."""
        result = (
            self.service.users().labels().get(userId="me", id=label_id).execute()
        )
        return {
            "id": result["id"],
            "name": result["name"],
            "type": result.get("type", "user"),
            "messages_total": result.get("messagesTotal", 0),
            "messages_unread": result.get("messagesUnread", 0),
            "threads_total": result.get("threadsTotal", 0),
            "threads_unread": result.get("threadsUnread", 0),
        }

    def create_label(
        self,
        name: str,
        message_list_visibility: str = "show",
        label_list_visibility: str = "labelShow",
    ) -> dict:
        """라벨 생성.

        Args:
            name: 라벨 이름
            message_list_visibility: 메시지 목록에서 표시 여부 (show, hide)
            label_list_visibility: 라벨 목록에서 표시 여부 (labelShow, labelHide)

        Returns:
            생성된 라벨 정보
        """
        body = {
            "name": name,
            "messageListVisibility": message_list_visibility,
            "labelListVisibility": label_list_visibility,
        }

        result = (
            self.service.users().labels().create(userId="me", body=body).execute()
        )

        return {
            "id": result["id"],
            "name": result["name"],
            "status": "created",
        }

    def update_label(
        self,
        label_id: str,
        name: Optional[str] = None,
        message_list_visibility: Optional[str] = None,
        label_list_visibility: Optional[str] = None,
    ) -> dict:
        """라벨 수정."""
        result = (
            self.service.users().labels().get(userId="me", id=label_id).execute()
        )

        if name:
            result["name"] = name
        if message_list_visibility:
            result["messageListVisibility"] = message_list_visibility
        if label_list_visibility:
            result["labelListVisibility"] = label_list_visibility

        updated = (
            self.service.users()
            .labels()
            .update(userId="me", id=label_id, body=result)
            .execute()
        )

        return {
            "id": updated["id"],
            "name": updated["name"],
            "status": "updated",
        }

    def delete_label(self, label_id: str) -> dict:
        """라벨 삭제."""
        self.service.users().labels().delete(userId="me", id=label_id).execute()
        return {
            "id": label_id,
            "status": "deleted",
        }

    # =========================================================================
    # Drafts
    # =========================================================================

    def list_drafts(self, max_results: int = 20) -> list[dict]:
        """초안 목록 조회."""
        drafts = []
        page_token = None

        while len(drafts) < max_results:
            kwargs = {
                "userId": "me",
                "maxResults": min(max_results - len(drafts), 100),
            }
            if page_token:
                kwargs["pageToken"] = page_token

            result = self.service.users().drafts().list(**kwargs).execute()

            for draft in result.get("drafts", []):
                drafts.append(draft)

            page_token = result.get("nextPageToken")
            if not page_token:
                break

        return drafts

    def get_draft(self, draft_id: str) -> dict:
        """초안 상세 조회."""
        result = (
            self.service.users()
            .drafts()
            .get(userId="me", id=draft_id, format="full")
            .execute()
        )

        return {
            "id": result["id"],
            "message": self._parse_message(result["message"]),
        }

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        html: bool = False,
    ) -> dict:
        """초안 생성.

        Args:
            to: 수신자
            subject: 제목
            body: 본문
            cc: 참조
            bcc: 숨은 참조
            html: HTML 형식 여부

        Returns:
            생성된 초안 정보
        """
        message = MIMEText(body, "html" if html else "plain", "utf-8")
        message["to"] = to
        message["subject"] = subject
        if cc:
            message["cc"] = cc
        if bcc:
            message["bcc"] = bcc

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        result = (
            self.service.users()
            .drafts()
            .create(userId="me", body={"message": {"raw": raw}})
            .execute()
        )

        return {
            "id": result["id"],
            "message_id": result["message"]["id"],
            "status": "created",
        }

    def send_draft(self, draft_id: str) -> dict:
        """초안 발송."""
        result = (
            self.service.users()
            .drafts()
            .send(userId="me", body={"id": draft_id})
            .execute()
        )

        return {
            "id": result["id"],
            "thread_id": result["threadId"],
            "label_ids": result.get("labelIds", []),
            "status": "sent",
        }

    def delete_draft(self, draft_id: str) -> dict:
        """초안 삭제."""
        self.service.users().drafts().delete(userId="me", id=draft_id).execute()
        return {
            "id": draft_id,
            "status": "deleted",
        }

    # =========================================================================
    # Profile
    # =========================================================================

    def get_profile(self) -> dict:
        """계정 프로필 조회."""
        @exponential_backoff(max_retries=5)
        def _get_profile():
            return self.service.users().getProfile(userId="me").execute()

        self._wait_for_quota(QuotaUnit.PROFILE_GET)
        result = _get_profile()
        self._record_quota(QuotaUnit.PROFILE_GET)

        return {
            "email": result["emailAddress"],
            "messages_total": result.get("messagesTotal", 0),
            "threads_total": result.get("threadsTotal", 0),
            "history_id": result.get("historyId", ""),
        }

    # =========================================================================
    # Batch Operations (P1)
    # =========================================================================

    def batch_get_messages(
        self,
        message_ids: list[str],
        format: str = "metadata",
    ) -> dict:
        """메시지 일괄 조회.

        Args:
            message_ids: 조회할 메시지 ID 목록
            format: 응답 형식 (minimal, full, raw, metadata)

        Returns:
            BatchResult 객체 (total, succeeded, failed, results, errors)
        """
        return self.batch_processor.batch_get_messages(message_ids, format)

    def batch_modify_labels(
        self,
        message_ids: list[str],
        add_labels: Optional[list[str]] = None,
        remove_labels: Optional[list[str]] = None,
    ) -> dict:
        """라벨 일괄 수정.

        Args:
            message_ids: 수정할 메시지 ID 목록
            add_labels: 추가할 라벨 ID
            remove_labels: 제거할 라벨 ID

        Returns:
            BatchResult 객체
        """
        result = self.batch_processor.batch_modify_labels(
            message_ids, add_labels, remove_labels
        )

        # Invalidate cache for modified messages
        if self._cache:
            for msg_id in message_ids:
                self._cache.invalidate_message(self.account_name, msg_id)
            self._cache.invalidate_lists(self.account_name)

        return result

    def batch_trash_messages(self, message_ids: list[str]) -> dict:
        """메시지 일괄 휴지통 이동.

        Args:
            message_ids: 휴지통으로 이동할 메시지 ID 목록

        Returns:
            BatchResult 객체
        """
        result = self.batch_processor.batch_trash_messages(message_ids)

        # Invalidate cache
        if self._cache:
            for msg_id in message_ids:
                self._cache.invalidate_message(self.account_name, msg_id)
            self._cache.invalidate_lists(self.account_name)

        return result

    def batch_delete_messages(self, message_ids: list[str]) -> dict:
        """메시지 일괄 영구 삭제.

        주의: 이 작업은 되돌릴 수 없습니다!

        Args:
            message_ids: 삭제할 메시지 ID 목록

        Returns:
            BatchResult 객체
        """
        result = self.batch_processor.batch_delete_messages(message_ids)

        # Invalidate cache
        if self._cache:
            for msg_id in message_ids:
                self._cache.invalidate_message(self.account_name, msg_id)
            self._cache.invalidate_lists(self.account_name)

        return result

    def mark_all_as_read(
        self,
        query: str = "is:unread",
        max_messages: int = 500,
    ) -> dict:
        """조건에 맞는 메시지 전체 읽음 처리.

        Args:
            query: 검색 쿼리 (기본: 읽지 않음)
            max_messages: 최대 처리 메시지 수

        Returns:
            BatchResult 객체
        """
        result = self.batch_processor.mark_all_as_read(query, max_messages)

        # Invalidate cache
        if self._cache:
            self._cache.invalidate_lists(self.account_name)

        return result

    def archive_all(
        self,
        query: str = "",
        max_messages: int = 500,
    ) -> dict:
        """조건에 맞는 메시지 전체 보관처리.

        Args:
            query: 검색 쿼리
            max_messages: 최대 처리 메시지 수

        Returns:
            BatchResult 객체
        """
        result = self.batch_processor.archive_all(query, max_messages)

        # Invalidate cache
        if self._cache:
            self._cache.invalidate_lists(self.account_name)

        return result

    # =========================================================================
    # Cache & Quota Management
    # =========================================================================

    def get_quota_status(self) -> dict:
        """현재 할당량 사용 현황 조회.

        Returns:
            할당량 사용 현황 딕셔너리
        """
        if self._quota_manager:
            return self._quota_manager.get_usage(self.account_name)
        return {"message": "Quota management is disabled"}

    def get_cache_stats(self) -> dict:
        """캐시 통계 조회.

        Returns:
            캐시 통계 딕셔너리
        """
        if self._cache:
            return self._cache.get_stats(self.account_name)
        return {"message": "Caching is disabled"}

    def clear_cache(self) -> None:
        """이 계정의 캐시 전체 삭제."""
        if self._cache:
            self._cache.invalidate_account(self.account_name)
            logger.info(f"Cache cleared for account: {self.account_name}")


class ADCGmailClient:
    """Application Default Credentials를 사용하는 Gmail 클라이언트.

    gcloud auth application-default login으로 인증된 계정 사용.
    """

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.labels",
    ]

    def __init__(self, account_name: str = "default", timeout: int = DEFAULT_TIMEOUT):
        self.account_name = account_name
        self.timeout = timeout
        self.creds, self.project = google.auth.default(scopes=self.SCOPES)
        self._service = None

    @property
    def service(self):
        if self._service is None:
            self._service = build("gmail", "v1", credentials=self.creds)
        return self._service

    def list_messages(
        self,
        query: str = "",
        max_results: int = 20,
        label_ids: Optional[list[str]] = None,
        include_spam_trash: bool = False,
    ) -> list[dict]:
        messages = []
        page_token = None

        while len(messages) < max_results:
            kwargs = {
                "userId": "me",
                "maxResults": min(max_results - len(messages), 100),
                "includeSpamTrash": include_spam_trash,
            }
            if query:
                kwargs["q"] = query
            if label_ids:
                kwargs["labelIds"] = label_ids
            if page_token:
                kwargs["pageToken"] = page_token

            result = self.service.users().messages().list(**kwargs).execute()

            for msg in result.get("messages", []):
                messages.append(msg)

            page_token = result.get("nextPageToken")
            if not page_token:
                break

        return messages

    def get_profile(self) -> dict:
        result = self.service.users().getProfile(userId="me").execute()
        return {
            "email": result["emailAddress"],
            "messages_total": result.get("messagesTotal", 0),
            "threads_total": result.get("threadsTotal", 0),
        }


def get_all_accounts(base_path: Optional[Path] = None) -> list[str]:
    """등록된 모든 계정 이름 반환."""
    base_path = base_path or Path(__file__).parent.parent
    accounts_dir = base_path / "accounts"

    if not accounts_dir.exists():
        return []

    return [
        f.stem for f in accounts_dir.glob("*.json") if f.stem not in ("credentials",)
    ]


def get_client(
    account_name: Optional[str] = None,
    use_adc: bool = False,
    base_path: Optional[Path] = None,
) -> GmailClient:
    """Gmail 클라이언트 팩토리.

    Args:
        account_name: 계정 이름 (None이면 첫 번째 계정 사용)
        use_adc: ADC 사용 여부
        base_path: skill 루트 경로

    Returns:
        GmailClient 또는 ADCGmailClient 인스턴스
    """
    if use_adc:
        return ADCGmailClient(account_name or "default")

    if account_name:
        return GmailClient(account_name, base_path)

    accounts = get_all_accounts(base_path)
    if not accounts:
        raise ValueError(
            "등록된 계정이 없습니다. setup_auth.py --account <이름> 실행 필요"
        )

    return GmailClient(accounts[0], base_path)
