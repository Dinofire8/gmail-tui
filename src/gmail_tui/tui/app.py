from textual.app import App
from gmail_tui.config import load_config
from gmail_tui.tui.screens.home import HomeScreen


class GmailApp(App):
    TITLE = "Gmail"
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.dark = False

    def get_css(self) -> str:
        t = self.cfg["theme"]
        return f"""
        Screen {{
            background: {t['background']};
            layers: base;
        }}
        HomeScreen {{
            background: {t['background']};
            align: center middle;
        }}
        Vertical {{
            background: transparent;
        }}
        Horizontal {{
            background: transparent;
        }}
        ListView {{
            background: transparent;
        }}
        #home-container {{
            align: center middle;
            width: 100%;
            height: 100%;
        }}
        #inbox-panel {{
            width: 35%;
            border: solid {t['border']};
        }}
        #email-panel {{
            width: 65%;
            border: solid {t['border']};
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
        #ascii-art {{
            color: {t['primary']};
            padding: 2 4;
        }}
        #version {{
            color: {t['text_muted']};
            padding: 0 4;
        }}
        #menu {{
            color: {t['text']};
            padding: 1 4;
        }}
        """

    def on_mount(self) -> None:
        self.app.stylesheet.add_source(self.get_css())
        self.push_screen(HomeScreen())


if __name__ == "__main__":
    app = GmailApp()
    app.run()