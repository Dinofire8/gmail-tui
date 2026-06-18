from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Vertical
from gmail_tui.config import VERSION

ASCII = """
  ██████╗ ███╗   ███╗ █████╗ ██╗██╗      ████████╗██╗   ██╗██╗
 ██╔════╝ ████╗ ████║██╔══██╗██║██║      ╚══██╔══╝██║   ██║██║
 ██║  ███╗██╔████╔██║███████║██║██║         ██║   ██║   ██║██║
 ██║   ██║██║╚██╔╝██║██╔══██║██║██║         ██║   ██║   ██║██║
 ╚██████╔╝██║ ╚═╝ ██║██║  ██║██║███████╗    ██║   ╚██████╔╝██║
  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝    ╚═════╝ ╚═╝
"""

MENU = """
  [1] Inbox
  [2] Sent
  [3] Contacts
  [4] Settings

  [q] Quit
"""


class HomeScreen(Screen):
    BINDINGS = [
        ("1", "goto_inbox", "Inbox"),
        ("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="home-container"):
            yield Static(ASCII, id="ascii-art")
            yield Static(f"  v{VERSION}", id="version")
            yield Static(MENU, id="menu")
        yield Footer()

    def action_goto_inbox(self) -> None:
        from gmail_tui.tui.screens.inbox import InboxScreen
        self.app.push_screen(InboxScreen())