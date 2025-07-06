from src.shared.log import log_to_file


class TermColor:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


def info(msg: str) -> None:
    print(f"{TermColor.BLUE}{msg}{TermColor.RESET}")
    log_to_file("info", msg)


def success(msg: str) -> None:
    print(f"{TermColor.GREEN}{msg}{TermColor.RESET}")
    log_to_file("success", msg)


def warn(msg: str) -> None:
    print(f"{TermColor.YELLOW}{msg}{TermColor.RESET}")
    log_to_file("warn", msg)


def error(msg: str) -> None:
    print(f"{TermColor.RED}{msg}{TermColor.RESET}")
    log_to_file("error", msg)
