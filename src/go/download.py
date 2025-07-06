import os
import tempfile
import urllib.request
from typing import Optional

from src.shared.log import log_to_file
from src.shared.term import error


def download(version: str, _os: str, arch: str) -> Optional[str]:
    filename = f"go{version}.{_os}-{arch}.tar.gz"
    url = f"https://go.dev/dl/{filename}"

    try:
        temp_dir = tempfile.mkdtemp(prefix="xvm-download-")
        dest_path = os.path.join(temp_dir, filename)

        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, dest_path)

        print(f"Downloaded to {dest_path}")
        return dest_path
    except Exception as e:
        error(f"Failed to download Go {version}")
        log_to_file('error', str(e))
        return None
