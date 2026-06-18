from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, Static
from textual.containers import Horizontal, Vertical
from gmail_tui.client import GmailClient
from gmail_tui.models import Email
from gmail_tui.config import load_config


class GmailApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()
        self.cfg = load_config()

    def get_css(self) -> str:
        t = self.cfg["theme"]
        return f"""
        Screen {{
            background: {t['background']};
        }}
        #inbox-panel {{
            width: 35%;
            border: solid {t['border']};
            background: {t['surface']};
        }}
        #email-panel {{
            width: 65%;
            border: solid {t['border']};
            background: {t['surface']};
        }}
        #inbox-label {{
            background: {t['secondary']};
            color: {t['text']};
            padding: 0 1;
        }}
        #email-content {{
            padding: 1 2;
            color: {t['text']};
        }}
        ListView {{
            background: {t['surface']};
        }}
        ListItem {{
            color: {t['text_muted']};
        }}
        ListItem:hover {{
            background: {t['secondary']};
            color: {t['text']};
        }}
        ListItem.--highlight {{
            background: {t['primary']};
            color: {t['text']};
        }}
        """

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="inbox-panel"):
                yield Label("Inbox", id="inbox-label")
                yield ListView(id="inbox")
            with Vertical(id="email-panel"):
                yield Static("Select an email", id="email-content")
        yield Footer()

    def on_mount(self) -> None:
        self.app.stylesheet.add_source(self.get_css())
        self.client = GmailClient()
        self.threads = []
        self.load_inbox()

    def load_inbox(self) -> None:
        self.threads = self.client.list_threads()
        inbox = self.query_one("#inbox", ListView)
        inbox.clear()
        for t in self.threads:
            inbox.append(ListItem(Label(t["snippet"][:60])))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        thread = self.threads[index]
        raw = self.client.get_email(thread["id"])
        email = Email.from_api(raw)
        content = self.query_one("#email-content", Static)
        content.update(
            f"From: {email.sender}\n"
            f"To: {email.to}\n"
            f"Date: {email.date}\n"
            f"Subject: {email.subject}\n\n"
            f"{email.snippet}"
        )

    def action_refresh(self) -> None:
        self.load_inbox()


if __name__ == "__main__":
    app = GmailApp()
    app.run()