import sys
from typing import Optional, List

from src.shared.term import error


def normalise_version(v: str) -> str:
    return v.lstrip("v")


def _parse_node_version(v: str) -> tuple:
    parts = v.lstrip("v").split(".")
    return tuple(int(p) for p in parts)


def get_latest_stable_version(installed: Optional[List[str]]) -> Optional[str]:
    if not installed:
        error('No installed versions found, exiting...')
        sys.exit(1)

    return installed[0]
