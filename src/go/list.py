import json
import os
import urllib.request
from typing import List, Optional

from src.go.utils import _parse_go_version, normalise_version
from src.shared.const import XVM_GO_DIR
from src.shared.log import log_to_file
from src.shared.term import error


def is_installed(version: str) -> bool:
    installed = list_installed_versions()
    if not installed:
        return False
    version = normalise_version(version)

    return version in installed


def list_installed_versions() -> Optional[List[str]]:
    try:
        res = []
        subdirs = os.listdir(XVM_GO_DIR)
        for _dir in subdirs:
            full_path = os.path.join(XVM_GO_DIR, _dir)
            if os.path.isdir(full_path):
                res.append(_dir)

        x = sorted(res, key=_parse_go_version, reverse=True)
        for i in range(len(x)):
            x[i] = normalise_version(x[i])

        return x
    except Exception as e:
        error(f"Failed to list installed versions")
        log_to_file('error', str(e))
        return None


def list_available_versions(_os: str, arch: str) -> Optional[List[str]]:
    url = "https://go.dev/dl/?mode=json&include=all"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        versions = set()
        for release in data:
            version = release.get("version")
            if not version:
                continue
            for file in release.get("files", []):
                if file.get("os") == _os and file.get("arch") == arch:
                    version = normalise_version(version)
                    versions.add(version)
                    break

        return sorted(versions, key=_parse_go_version, reverse=True)
    except Exception as e:
        error(f"Failed to fetch Go versions")
        log_to_file('error', str(e))
        return None
