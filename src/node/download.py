import os
import tempfile
import urllib.request
from typing import Optional

from src.node.utils import normalise_version
from src.shared.log import log_to_file
from src.shared.term import error


def download(version: str, _os: str, arch: str) -> Optional[str]:
    version = normalise_version(version)
    version = f"v{version}"

    ext = "zip" if _os == "Windows" else "tar.xz"
    filename = f"node-{version}-{_os}-{arch}.{ext}"
    url = f"https://nodejs.org/dist/{version}/{filename}"

    try:
        temp_dir = tempfile.mkdtemp(prefix="xvm-node-download-")
        dest_path = os.path.join(temp_dir, filename)

        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, dest_path)

        print(f"Downloaded to {dest_path}")
        return dest_path
    except Exception as e:
        error(f"Failed to download Node.js {version}")
        log_to_file('error', str(e))
        return None
