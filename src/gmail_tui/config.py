from pathlib import Path
import json

DEFAULT_CONFIG = {
    "theme": {
        "primary": "#9b59b6",
        "secondary": "#6c3483",
        "background": "#1a1a2e",
        "surface": "#16213e",
        "text": "#e0e0e0",
        "text_muted": "#888888",
        "border": "#9b59b6",
        "highlight": "#a855f7",
    },
    "inbox": {
        "max_results": 20,
        "preview_length": 60,
    }
}

CONFIG_PATH = Path.home() / ".config" / "gmail-tui" / "config.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            user = json.load(f)
        # merge with defaults so missing keys still work
        merged = DEFAULT_CONFIG.copy()
        for key in user:
            merged[key].update(user[key])
        return merged
    return DEFAULT_CONFIG.copy()


def create_default_config():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"Config created at {CONFIG_PATH}")
