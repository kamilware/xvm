import os
import subprocess
import sys

from src.node.install import install, send_notification
from src.node.list import list_installed_versions, list_available_versions, is_installed
from src.node.rc import activate
from src.node.uninstall import uninstall
from src.node.update import setup_autoupdate_service, remove_autoupdate_service, SYSTEMD_SERVICE_PATH, \
    SYSTEMD_SERVICE_NAME
from src.node.utils import normalise_version, get_latest_stable_version
from src.shared.const import SUPPORTED_COMMANDS
from src.shared.log import log_to_file
from src.shared.system_info import get_system_info
from src.shared.term import error, TermColor, info, warn


def print_versions() -> None:
    installed_versions = list_installed_versions()
    sys_info = get_system_info('node')
    available_versions = list_available_versions(sys_info["os"], sys_info["arch"])

    info(f'Found {len(installed_versions)} installed versions, available: {len(available_versions)}')

    for version in available_versions:
        if version in installed_versions:
            version = normalise_version(version)
            print(f"- {TermColor.GREEN}{version} (installed){TermColor.RESET}")
        else:
            print(f"- {TermColor.RED}{version} (not installed){TermColor.RESET}")


def handle(args):
    command = args[1].lower()
    if command not in SUPPORTED_COMMANDS:
        error(f'Command {command} is not supported, exiting...')
        sys.exit(1)

    if command == "list":
        print_versions()
    elif command == "install":
        version = ''

        try:
            version = args[2].lower()
            version = normalise_version(version)
        except Exception as e:
            log_to_file('error', str(e))
            error("Incorrect args, exiting...")
            sys.exit(1)

        if is_installed(version):
            warn(f'Version {version} is already installed...')
        else:
            install(version)
    elif command == 'uninstall':
        version = ''

        try:
            version = args[2].lower()
            version = normalise_version(version)
        except Exception as e:
            log_to_file('error', str(e))
            error("Incorrect args, exiting...")
            sys.exit(1)

        if is_installed(version):
            uninstall(version)
        else:
            warn(f'Version {version} is not installed...')
    elif command == 'active':
        try:
            version = args[2].lower()
        except Exception as e:
            log_to_file('error', str(e))
            error("Incorrect args, exiting...")
            sys.exit(1)

        if version == 'latest':
            version = get_latest_stable_version(list_installed_versions())

        version = normalise_version(version)

        if is_installed(version):
            activate(version)
        else:
            warn(f'Version {version} is not installed...')
    elif command == 'autoupdate':
        try:
            subcommand = args[2].lower()
        except IndexError:
            if os.path.exists(SYSTEMD_SERVICE_PATH):
                status = subprocess.run(
                    ["systemctl", "--user", "is-enabled", SYSTEMD_SERVICE_NAME],
                    capture_output=True, text=True
                )
                if "enabled" in status.stdout:
                    info("Auto-update is currently: ON")
                else:
                    info("Auto-update service is present but not enabled.")
            else:
                info("Auto-update is currently: OFF")
            return

        if subcommand == "on":
            setup_autoupdate_service()
        elif subcommand == "off":
            remove_autoupdate_service()
        else:
            error(f"Unknown subcommand: '{subcommand}'. Use 'on', 'off', or no argument.")
