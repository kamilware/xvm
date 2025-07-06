import os
import shutil

from src.node.rc import remove_export, remove_alias
from src.node.utils import normalise_version
from src.shared.const import XVM_GO_DIR
from src.shared.log import log_to_file
from src.shared.term import success, error


def uninstall(version: str):
    version = normalise_version(version)
    install_path = os.path.join(XVM_GO_DIR, version)

    if not os.path.exists(install_path):
        error(f"Node {version} is not installed at {install_path}")
        return

    try:
        shutil.rmtree(install_path)
        success(f"Removed {install_path}")
    except Exception as e:
        error(f"Failed to remove {install_path}")
        log_to_file('error', str(e))
        return

    remove_alias(version)
    remove_export()
