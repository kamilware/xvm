import os
import sys

from src.shared.const import SUPPORTED_SHELLS, SUPPORTED_OS, SUPPORTED_ARCH, XVM_GO_DIR, XVM_DIR, XVM_NODE_DIR
from src.shared.log import log_to_file
from src.shared.system_info import get_system_info, SystemInfo
from src.shared.term import info as t_info, error, success


def support_check() -> SystemInfo:
    info = get_system_info('')

    t_info(f'Your configuration: {info["arch"]} {info["os"]}({info["distro"]}), {info["shell"]}')

    if info["arch"] not in SUPPORTED_ARCH:
        error(f'{info["arch"]} is not supported, exiting...')
        sys.exit(1)
    elif info["os"] not in SUPPORTED_OS:
        error(f'{info["os"]} is not supported, exiting...')
        sys.exit(1)
    elif info["shell"] not in SUPPORTED_SHELLS:
        error(f'{info["shell"]} is not supported, exiting...')
        sys.exit(1)

    success('Your configuration is supported')
    return info


def scaffold():
    try:
        os.makedirs(XVM_DIR, exist_ok=True)
        os.makedirs(XVM_GO_DIR, exist_ok=True)
        os.makedirs(XVM_NODE_DIR, exist_ok=True)
    except Exception as e:
        error(f'Error scaffolding xvm, exiting...')
        log_to_file('error', str(e))
