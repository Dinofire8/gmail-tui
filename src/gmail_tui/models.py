import base64
from dataclasses import dataclass, field


def _decode_body(payload: dict) -> str:
    data = payload.get("body", {}).get("data", "")
    if data:
        return base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
    for part in payload.get("parts", []):
        if part.get("parts"):
            result = _decode_body(part)
            if result:
                return result
    return ""


@dataclass
class Email:
    id: str
    thread_id: str
    subject: str
    sender: str
    to: str
    date: str
    body: str
    snippet: str
    label_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict) -> "Email":
        id = data["id"]
        thread_id = data["threadId"]
        snippet = data.get("snippet", "")
        label_ids = data.get("labelIds", [])
        payload = data.get("payload", {})
        headers = payload.get("headers", [])

        def get_header(name: str) -> str:
            for h in headers:
                if h["name"].lower() == name.lower():
                    return h["value"]
            return ""

        return cls(
            id=id,
            thread_id=thread_id,
            subject=get_header("Subject"),
            sender=get_header("From"),
            to=get_header("To"),
            date=get_header("Date"),
            body=_decode_body(payload),
            snippet=snippet,
            label_ids=label_ids,
        )


@dataclass
class Thread:
    id: str
    messages: list[Email] = field(default_factory=list)
    snippet: str = ""
    label_ids: list[str] = field(default_factory=list)


@dataclass
class Label:
    id: str
    name: str