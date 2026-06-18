import base64
from dataclasses import dataclass, field


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

        headers = data["payload"]["headers"]

        def get_header(name: str) -> str:
            for h in headers:
                if h["name"].lower() == name.lower():
                    return h["value"]
            return ""

        subject = get_header("Subject")
        sender = get_header("From")
        to = get_header("To")
        date = get_header("Date")

        return cls(
            id=id,
            thread_id=thread_id,
            subject=subject,
            sender=sender,
            to=to,
            date=date,
            body="",
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