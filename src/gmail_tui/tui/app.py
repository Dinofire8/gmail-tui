from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label
from gmail_tui.client import GmailClient


class GmailApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(id="inbox")
        yield Footer()

    def on_mount(self) -> None:
        self.client = GmailClient()
        self.load_inbox()

    def load_inbox(self) -> None:
        threads = self.client.list_threads()
        inbox = self.query_one("#inbox", ListView)
        for t in threads:
            inbox.append(ListItem(Label(t["snippet"][:60])))


if __name__ == "__main__":
    app = GmailApp()
    app.run()
