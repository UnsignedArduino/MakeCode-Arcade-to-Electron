import logging
from pathlib import Path
from zipfile import ZipFile

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def extract(src: Path, dest: Path):
    """
    Extract a zip file to a destination path.

    :param src: The source zip file to extract.
    :param dest: The destination path to extract the zip file to.
    """
    logger.debug(f"Extracting {src} to {dest}")
    with ZipFile(src, "r") as z:
        z.extractall(dest)
    logger.debug(f"Extracted {src} to {dest}")
