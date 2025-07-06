import os
import tarfile

from src.go.download import download
from src.go.list import list_available_versions
from src.go.rc import remove_export, add_alias, add_export
from src.go.utils import normalise_version
from src.shared.const import XVM_GO_DIR, SUPPORTED_SHELLS
from src.shared.log import log_to_file
from src.shared.notification import send_notification
from src.shared.system_info import get_system_info
from src.shared.term import info, success, error


def install(version: str):
    sys_info = get_system_info('go')
    version = normalise_version(version)

    if sys_info["shell"] not in SUPPORTED_SHELLS:
        error(f"Shell '{sys_info['shell']}' is not supported yet.")
        return

    if version == 'latest':
        available_versions = list_available_versions(sys_info["os"], sys_info["arch"])
        if not available_versions:
            error("No available versions found.")
            return
        for v in available_versions:
            if "rc" not in v and "beta" not in v:
                version = v
                break
        else:
            error("No stable version found.")
            return

    install_path = os.path.join(XVM_GO_DIR, version)
    if os.path.exists(install_path):
        info(f"go{version} is already installed at {install_path}")
        return

    archive_path = download(version, sys_info["os"], sys_info["arch"])
    if not archive_path:
        error("Download failed.")
        return

    info(f"Extracting to {install_path}...")
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=XVM_GO_DIR)

        os.rename(os.path.join(XVM_GO_DIR, "go"), install_path)
        success(f"go{version} installed to {install_path}")
    except Exception as e:
        error(f"Extraction failed")
        log_to_file('error', str(e))
        return

    remove_export()

    try:
        add_alias(version, install_path)
        add_export(install_path)
        success("Config successfully updated, please reopen your terminal")
    except Exception as e:
        error("Error during updating config")
        log_to_file('error', str(e))

    send_notification("XVM Go", f"go{version} installed successfully", sys_info)
