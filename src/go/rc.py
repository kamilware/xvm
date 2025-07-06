import os
from typing import Optional

from src.go.utils import normalise_version
from src.shared.const import XVM_GO_DIR
from src.shared.log import log_to_file
from src.shared.shell import get_rc_file
from src.shared.term import error, success


def ensure_alias(version: str):
    rc_path = get_rc_file()
    version = normalise_version(version)
    path = os.path.join(XVM_GO_DIR, version)
    s = f'alias go{version}="{path}/bin/go"\n'

    try:
        with open(rc_path, "a") as f:
            lines = f.readlines()

            if s in lines:
                return

            f.write(s)
    except Exception as e:
        error(f"Failed to write to {rc_path}")
        log_to_file('error', str(e))


def add_alias(version: str, path: str):
    rc_path = get_rc_file()
    version = normalise_version(version)
    s = f'alias go{version}="{path}/bin/go"\n'

    try:
        with open(rc_path, "a") as f:
            f.write(s)
    except Exception as e:
        error(f"Failed to write to {rc_path}")
        log_to_file('error', str(e))


def add_export(path: str):
    rc_path = get_rc_file()

    try:
        with open(rc_path, "a") as f:
            f.write(f'export GOROOT="{path}"\n')
            f.write(f'export PATH="$GOROOT/bin:$PATH"\n')
    except Exception as e:
        log_to_file('error', str(e))


def remove_export():
    rc_path = get_rc_file()

    try:
        with open(rc_path, "r") as f:
            lines = f.readlines()

        with open(rc_path, "w") as f:
            for line in lines:
                if "GOROOT=" in line or "$GOROOT/bin" in line or "GOROOT =" in line:
                    continue
                f.write(line)
    except Exception as e:
        error(f"Failed to clean old Go settings from {rc_path}")
        log_to_file('error', str(e))


def remove_alias(version: str):
    rc_path = get_rc_file()
    version = normalise_version(version)

    try:
        with open(rc_path, "r") as f:
            lines = f.readlines()

        with open(rc_path, "w") as f:
            for line in lines:
                if "alias" in line and f"go{version}" in line:
                    continue
                f.write(line)
    except Exception as e:
        error(f"Failed to clean old Go settings from {rc_path}")
        log_to_file('error', str(e))


def get_path(version: str) -> Optional[str]:
    rc_path = get_rc_file()
    version = normalise_version(version)

    try:
        with open(rc_path, "r") as f:
            lines = f.readlines()

            for line in lines:
                if "alias" in line and f"go{version}" in line:
                    return line
    except Exception as e:
        error(f"Failed retrieve installation dir for {version}")
        log_to_file('error', str(e))


def activate(version: str):
    version = normalise_version(version)

    path = os.path.join(XVM_GO_DIR, version)
    remove_export()

    add_export(path)

    success(f'Version {version} successfully activated, please reopen your terminal')
