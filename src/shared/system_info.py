import os
import platform
from typing import TypedDict

from src.shared.const import GO_ARCH_MAP, NODE_ARCH_MAP


class SystemInfo(TypedDict):
    os: str
    distro: str
    arch: str
    shell: str


def get_system_info(target: str) -> SystemInfo:
    os_name = platform.system()
    arch = platform.machine()

    distro = ""
    if os_name == "Linux":
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.strip().split("=")[1].strip('"')
                        break
        except FileNotFoundError:
            distro = "unknown"
    elif os_name == "Darwin":
        distro = "macOS"
    elif os_name == "Windows":
        distro = "Windows"
    else:
        distro = "unknown"

    shell = os.environ.get("SHELL", "unknown")
    shell = os.path.basename(shell)

    if target == 'go':
        if arch in GO_ARCH_MAP:
            arch = GO_ARCH_MAP[arch]
    elif target == 'node':
        if arch in NODE_ARCH_MAP:
            arch = NODE_ARCH_MAP[arch]

    return {
        "os": os_name.lower(),
        "distro": distro.lower(),
        "arch": arch.lower(),
        "shell": shell.lower(),
    }
