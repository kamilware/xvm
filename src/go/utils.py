import re
import sys
from typing import Optional, List

from src.shared.term import error


def _parse_go_version(v: str) -> tuple:
    match = re.match(r"(\d+)\.(\d+)(?:\.(\d+))?(rc|beta)?(\d+)?", v)
    if not match:
        return 0, 0, 0, '', 0

    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3) or 0)
    pre_rel = match.group(4) or ''
    pre_num = int(match.group(5) or 0)

    pre_order = {'': 0, 'beta': -2, 'rc': -1}
    return major, minor, patch, pre_order[pre_rel], pre_num


def normalise_version(version: str) -> str:
    return version.removeprefix("go")


def get_latest_stable_version(installed: Optional[List[str]]) -> Optional[str]:
    if not installed:
        error('No installed versions found, exiting...')
        sys.exit(1)

    for v in installed:
        if not 'rc' in v or 'beta' in v:
            return v

    return None
