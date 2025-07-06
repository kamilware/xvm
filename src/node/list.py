import json
import os
import urllib.request
from typing import Optional, List

from src.node.utils import normalise_version, _parse_node_version
from src.shared.const import XVM_NODE_DIR
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
        subdirs = os.listdir(XVM_NODE_DIR)
        for _dir in subdirs:
            full_path = os.path.join(XVM_NODE_DIR, _dir)
            if os.path.isdir(full_path):
                res.append(_dir)

        x = sorted(res, key=_parse_node_version, reverse=True)
        for i in range(len(x)):
            x[i] = normalise_version(x[i])

        return x
    except Exception as e:
        error(f"Failed to list installed versions")
        log_to_file('error', str(e))
        return None


def list_available_versions(_os: str, arch: str) -> Optional[List[str]]:
    url = "https://nodejs.org/dist/index.json"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        versions = []
        for release in data:
            version = release.get("version")
            files = release.get("files", [])

            platform_key = f"{_os}-{arch}"
            if platform_key in files:
                versions.append(normalise_version(version))

        return sorted(versions, key=_parse_node_version, reverse=True)
    except Exception as e:
        error("Failed to fetch Node versions")
        log_to_file("error", str(e))
        return None
