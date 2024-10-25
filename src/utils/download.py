import logging
from pathlib import Path

import requests
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def download(url: str, dest: Path):
    """
    Download a file from a URL to a destination path.

    :param url: The URL to download from.
    :param dest: The destination path to save the file to.
    """
    logger.debug(f"Downloading {url} to {dest}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    logger.debug(f"Downloaded {url} to {dest}")
