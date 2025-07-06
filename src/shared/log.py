from datetime import datetime

from src.shared.const import LOG_PATH


def log_to_file(level: str, msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {level.upper()}: {msg}\n")
