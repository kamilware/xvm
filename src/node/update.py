import os
import plistlib
import subprocess

from src.shared.log import log_to_file
from src.shared.system_info import get_system_info
from src.shared.term import info, error

SYSTEMD_SERVICE_NAME = 'xvm-node-autoupdate.service'
SYSTEMD_SERVICE_PATH = os.path.expanduser(f"~/.config/systemd/user/{SYSTEMD_SERVICE_NAME}")
SYSTEMD_SERVICE_CONTENT = f"""[Unit]
Description=XVM Node Auto Update

[Service]
ExecStart=%h/.local/bin/xvm node install latest
Restart=on-failure

[Install]
WantedBy=default.target
"""

LAUNCHD_LABEL = "xvm.node.autoupdate"
LAUNCHD_PLIST_PATH = os.path.expanduser(f"~/Library/LaunchAgents/{LAUNCHD_LABEL}.plist")

XVM_EXEC_PATH = os.path.expanduser("~/.local/bin/xvm")

WINDOWS_TASK_NAME = "XVMNodeAutoUpdate"
WINDOWS_COMMAND = f'"{XVM_EXEC_PATH}" node install latest'


def setup_autoupdate_service():
    sys_info = get_system_info('')

    if sys_info["os"] == "linux":
        os.makedirs(os.path.dirname(SYSTEMD_SERVICE_PATH), exist_ok=True)

        with open(SYSTEMD_SERVICE_PATH, "w") as f:
            f.write(SYSTEMD_SERVICE_CONTENT)

        try:
            subprocess.run(["systemctl", "--user", "daemon-reexec"], check=True)
            subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "--user", "enable", "--now", SYSTEMD_SERVICE_NAME], check=True)
            info("Auto-update systemd service has been created and started.")
        except subprocess.CalledProcessError as e:
            log_to_file('error', str(e))
            error("Failed to create or start systemd service.")

    elif sys_info["os"] == "darwin":
        plist = {
            "Label": LAUNCHD_LABEL,
            "ProgramArguments": [XVM_EXEC_PATH, "node", "install", "latest"],
            "RunAtLoad": True,
            "KeepAlive": False,
            "StandardOutPath": os.path.expanduser("~/Library/Logs/xvm-node-autoupdate.log"),
            "StandardErrorPath": os.path.expanduser("~/Library/Logs/xvm-node-autoupdate.err"),
        }

        os.makedirs(os.path.dirname(LAUNCHD_PLIST_PATH), exist_ok=True)

        with open(LAUNCHD_PLIST_PATH, "wb") as f:
            plistlib.dump(plist, f)

        try:
            subprocess.run(["launchctl", "load", LAUNCHD_PLIST_PATH], check=True)
            info("Auto-update launchd agent has been created and loaded.")
        except subprocess.CalledProcessError as e:
            log_to_file('error', str(e))
            error("Failed to load launchd agent.")

    elif sys_info["os"] == "windows":
        try:
            subprocess.run([
                "schtasks", "/Create",
                "/TN", WINDOWS_TASK_NAME,
                "/TR", f'cmd /c {WINDOWS_COMMAND}',
                "/SC", "ONLOGON",
                "/RL", "LIMITED",
                "/F"
            ], check=True)
            info("Auto-update scheduled task has been created.")
        except subprocess.CalledProcessError as e:
            log_to_file('error', str(e))
            error("Failed to create scheduled task.")


def remove_autoupdate_service():
    sys_info = get_system_info('')

    if sys_info["os"] == "linux":
        try:
            subprocess.run(["systemctl", "--user", "disable", "--now", SYSTEMD_SERVICE_NAME], check=True)
            if os.path.exists(SYSTEMD_SERVICE_PATH):
                os.remove(SYSTEMD_SERVICE_PATH)
            info("Auto-update systemd service has been disabled and removed.")
        except subprocess.CalledProcessError as e:
            log_to_file('error', str(e))
            error("Failed to disable or remove systemd service.")

    elif sys_info["os"] == "darwin":
        try:
            subprocess.run(["launchctl", "unload", LAUNCHD_PLIST_PATH], check=True)
            if os.path.exists(LAUNCHD_PLIST_PATH):
                os.remove(LAUNCHD_PLIST_PATH)
            info("Auto-update launchd agent has been unloaded and removed.")
        except subprocess.CalledProcessError as e:
            log_to_file('error', str(e))
            error("Failed to unload or remove launchd agent.")

    elif sys_info["os"] == "windows":
        try:
            subprocess.run(["schtasks", "/Delete", "/TN", WINDOWS_TASK_NAME, "/F"], check=True)
            info("Auto-update scheduled task has been removed.")
        except subprocess.CalledProcessError as e:
            log_to_file('error', str(e))
            error("Failed to remove scheduled task.")
