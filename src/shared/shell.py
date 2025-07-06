import os

from src.shared.system_info import get_system_info


def get_rc_file() -> str:
    sys_info = get_system_info('')

    if sys_info['shell'] == 'bash':
        return os.path.expanduser("~/.bashrc")

    return ''
