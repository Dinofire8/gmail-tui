import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from googleapiclient.discovery import build
from gmail_tui.auth import get_credentials

_local = threading.local()


class GmailClient:
    def __init__(self):
        self.creds = get_credentials()
        self.service = build("gmail", "v1", credentials=self.creds)
        self.user = "me"

    def _thread_service(self):
        if not hasattr(_local, "service"):
            _local.service = build("gmail", "v1", credentials=self.creds)
        return _local.service

    def list_threads(self, label: str = "INBOX", max_results: int = 20) -> list[dict]:
        res = (
            self.service.users().threads().list(
                userId=self.user, labelIds=[label], maxResults=max_results
            ).execute()
        )
        thread_ids = [t["id"] for t in res.get("threads", [])]

        def fetch_meta(tid: str) -> dict:
            svc = self._thread_service()
            return (
                svc.users().threads().get(
                    userId=self.user,
                    id=tid,
                    format="metadata",
                    metadataHeaders=["From", "Subject", "Date"],
                ).execute()
            )

        results: list[dict | None] = [None] * len(thread_ids)
        with ThreadPoolExecutor(max_workers=10) as pool:
            futures = {pool.submit(fetch_meta, tid): i for i, tid in enumerate(thread_ids)}
            for future in as_completed(futures):
                results[futures[future]] = future.result()
        return results  # type: ignore[return-value]

    def get_thread(self, thread_id: str) -> dict:
        return (
            self.service.users().threads().get(
                userId=self.user, id=thread_id, format="full"
            ).execute()
        )

    def get_email(self, msg_id: str) -> dict:
        return (
            self.service.users().messages().get(
                userId=self.user, id=msg_id
            ).execute()
        )
