import json
import logging
import re
from pathlib import Path
from shutil import copyfile

from app.app_strings import FORGE_CONFIG_JS_CONTENTS, PACKAGE_JSON_CONTENTS, \
    SRC___INDEX_HTML_CONTENTS, SRC___MAIN_JS_CONTENTS
from bs4 import BeautifulSoup
from utils.download import download
from utils.extract import extract
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def create_app(app_path: Path, name: str, description: str, version: str, author: str):
    """
    Create the app.

    :param app_path: Path to a directory where the app will be created. This path
     should not exist.
    :param name: The name of the app.
    :param description: The description of the app.
    :param version: The version of the app. Should not include the "v".
    :param author: The author of the app.
    """
    logger.info("Creating app files")
    app_path.mkdir(parents=True, exist_ok=False)

    package_json_path = app_path / "package.json"
    package_json = PACKAGE_JSON_CONTENTS.replace("<NAME>", name)
    package_json = package_json.replace("<DESCRIPTION>", description)
    package_json = package_json.replace("<VERSION>", version)
    package_json = package_json.replace("<AUTHOR>", author)
    package_json_path.write_text(package_json)

    forge_config_js_path = app_path / "forge.config.js"
    forge_config_js_path.write_text(FORGE_CONFIG_JS_CONTENTS)

    src_path = app_path / "src"
    src_path.mkdir()

    main_js_path = src_path / "main.js"
    main_js_path.write_text(SRC___MAIN_JS_CONTENTS)

    index_html_path = src_path / "index.html"
    index_html = SRC___INDEX_HTML_CONTENTS.replace("<NAME>", name)
    index_html = index_html.replace("<VERSION>", version)
    index_html_path.write_text(index_html)

    fake_net_path = src_path / "fake-net"
    fake_net_path.mkdir()


def download_and_extract_game(temp_dir: Path, repo: str, version: str) -> Path:
    """
    Download and extract the game from the specified repo and version.

    :param temp_dir: The temporary directory to download and extract the game to.
    :param repo: The repo to download the game from.
    :param version: The version of the game to download.
    :return: The path to the extracted game.
    """
    url = f"https://github.com/{repo}/archive/refs/tags/v{version}.zip"
    logger.info(f"Downloading {url}")

    zip_path = temp_dir / "game.zip"
    download(url, zip_path)

    logger.info(f"Extracting {zip_path}")
    extract_dir = temp_dir / "game"
    extract(zip_path, extract_dir)

    repo_path = list(extract_dir.glob("*"))[0]
    logger.debug(f"Found repo path {repo_path}")
    return repo_path


def copy_bin_js(repo_path: Path, app_path: Path) -> Path:
    """
    Copy the binary.js file from the repo to the app.

    :param repo_path: The path to the extracted repo.
    :param app_path: The path to the app template.
    :return: The path to the binary.js file.
    """
    old_bin_js_path = repo_path / "assets" / "js" / "binary.js"
    new_bin_js_path = app_path / "src" / "binary.js"
    logger.info(f"Copying {old_bin_js_path} to {new_bin_js_path}")
    copyfile(old_bin_js_path, new_bin_js_path)
    return new_bin_js_path


def extract_sim_url(bin_js_path: Path) -> str:
    """
    Extract the simulator URL from the binary.js file.

    :param bin_js_path: The path to the binary.js file.
    :return: The simulator URL.
    """
    logger.info(f"Extracting simulator URL from {bin_js_path}")
    bin_js = bin_js_path.read_text()
    regex = re.compile(r"^//\s+meta=([^\n]+)\n", re.MULTILINE)
    match = regex.search(bin_js)
    metadata = json.loads(match.group(1))
    sim_url = metadata["simUrl"]
    logger.debug(f"Found simulator URL {sim_url}")
    return sim_url


def download_simulator_html_and_service_worker(app_path: Path, sim_url: str) -> Path:
    """
    Download ---simulator and ---simserviceworker files from the sim URL.

    :param app_path: The path to the app template.
    :param sim_url: The simulator URL.
    :return: The path to ---simulator.html.
    """
    logger.info(f"Downloading {sim_url}")
    simulator_html_path = app_path / "src" / "fake-net" / "---simulator.html"
    download(sim_url, simulator_html_path)

    simserviceworker_url = sim_url.replace("---simulator", "---simserviceworker")
    logger.info(f"Downloading {simserviceworker_url}")
    simserviceworker_js_path = app_path / "src" / "fake-net" / "---simserviceworker.js"
    download(simserviceworker_url, simserviceworker_js_path)

    return simulator_html_path


def find_css_to_download(html: str) -> list[str]:
    """
    Find all CSS files to download from the HTML.

    :param html: The HTML to search for CSS files.
    :return: A list of CSS files to download.
    """
    logger.info(f"Finding CSS files to download")
    soup = BeautifulSoup(html, features="html.parser")
    css_links = soup.find_all("link", rel="stylesheet")
    logger.debug(f"Found {len(css_links)} CSS links")
    return [link["href"] for link in css_links]


def find_js_to_download(html: str) -> list[str]:
    """
    Find all JS files to download from the HTML.

    :param html: The HTML to search for JS files.
    :return: A list of JS files to download.
    """
    logger.info(f"Finding JS files to download")
    soup = BeautifulSoup(html, features="html.parser")
    js_links = soup.find_all("script", src=True)
    logger.debug(f"Found {len(js_links)} scripts")
    return [link["src"] for link in js_links]
