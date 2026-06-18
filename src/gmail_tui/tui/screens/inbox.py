from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static
from textual.containers import Horizontal, Vertical
from textual import work
from gmail_tui.client import GmailClient
from gmail_tui.models import Email


def _get_header(headers: list[dict], name: str) -> str:
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _thread_label(thread: dict) -> str:
    messages = thread.get("messages", [])
    if not messages:
        return thread.get("snippet", "")[:70]
    headers = messages[-1].get("payload", {}).get("headers", [])
    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    if "<" in sender:
        sender = sender.split("<")[0].strip().strip('"')
    return f"{sender:<25} {subject}"[:72]


class InboxScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="inbox-panel"):
                yield Label("Loading...", id="inbox-label")
                yield ListView(id="inbox")
            with Vertical(id="email-panel"):
                yield Static("Select an email", id="email-content")
        yield Footer()

    def on_mount(self) -> None:
        self.client = GmailClient()
        self.threads: list[dict] = []
        self._fetch_inbox()

    @work(thread=True)
    def _fetch_inbox(self) -> None:
        threads = self.client.list_threads()

        def update() -> None:
            self.threads = threads
            self.query_one("#inbox-label", Label).update("Inbox")
            inbox = self.query_one("#inbox", ListView)
            inbox.clear()
            for t in threads:
                inbox.append(ListItem(Label(_thread_label(t))))

        self.app.call_from_thread(update)

    @work(thread=True)
    def _fetch_email(self, thread: dict) -> None:
        full = self.client.get_thread(thread["id"])
        messages = full.get("messages", [])
        if not messages:
            return
        email = Email.from_api(messages[-1])
        text = (
            f"From: {email.sender}\n"
            f"To: {email.to}\n"
            f"Date: {email.date}\n"
            f"Subject: {email.subject}\n"
            f"{'─' * 60}\n\n"
            f"{email.body or email.snippet}"
        )

        def update() -> None:
            self.query_one("#email-content", Static).update(text)

        self.app.call_from_thread(update)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        if index is None or index >= len(self.threads):
            return
        self.query_one("#email-content", Static).update("Loading...")
        self._fetch_email(self.threads[index])

    def action_refresh(self) -> None:
        self.query_one("#inbox-label", Label).update("Loading...")
        self._fetch_inbox()
