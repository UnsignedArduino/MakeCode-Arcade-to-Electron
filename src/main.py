import logging
import subprocess
import tempfile
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory

import app_builder
from app_args import add_app_args
from utils.download import download
from utils.logger import create_logger, set_all_stdout_logger_levels

parser = ArgumentParser(prog="MakeCode-Arcade-to-Electron",
                        description="A program to convert MakeCode Arcade games to "
                                    "Electron apps.")
add_app_args(parser)
args = parser.parse_args()

logger = create_logger(name=__name__, level=logging.INFO)
set_all_stdout_logger_levels(args.debug)
logger.debug(f"Received arguments: {args}")


def run_cmd(cmd: str, cwd: Path = None):
    logger.info(f"Running command {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


# TODO: Delete the temporary directory, don't override OS tempdir
tempfile.tempdir = Path.cwd()
with TemporaryDirectory(delete=False) as temp_dir:
    temp_dir = Path(temp_dir.decode())
    logger.debug(f"Created temporary directory {temp_dir}")

    app_path = app_builder.copy_app_template(temp_dir)
    app_builder.substitute_file_values(app_path, args)
    repo_path = app_builder.download_and_extract_game(temp_dir, args.repo, args.version)
    new_bin_js_path = app_builder.copy_bin_js(repo_path, app_path)
    sim_url = app_builder.extract_sim_url(new_bin_js_path)
    sim_html_path = app_builder.download_simulator_html_and_service_worker(app_path,
                                                                           sim_url)
    css_to_download = app_builder.find_css_to_download(sim_html_path.read_text())
    for css_url in css_to_download:
        end_part = css_url.split("/")[-1]
        css_path = app_path / "src" / "fake-net" / end_part
        logger.info(f"Downloading {css_url} to {css_path}")
        download(css_url, css_path)
    js_to_download = app_builder.find_js_to_download(sim_html_path.read_text())
    for js_url in js_to_download:
        end_part = js_url.split("/")[-1]
        js_path = app_path / "src" / "fake-net" / end_part
        logger.info(f"Downloading {js_url} to {js_path}")
        download(js_url, js_path)
    if args.icon:
        logger.info(f"Converting icon {args.icon} to .ico, .png, and .icns")
        src_icon_path = Path(args.icon).expanduser().resolve().absolute()
        dest_ico_path = (app_path / "src" / "icon.ico").resolve().absolute()
        dest_png_path = (app_path / "src" / "icon.png").resolve().absolute()
        dest_icns_path = (app_path / "src" / "icon.icns").resolve().absolute()
        run_cmd(
            f"magick convert {src_icon_path} -define icon:auto-resize=16,32,48,64,128,256 -compress zip {dest_ico_path}")
        run_cmd(f"magick convert {src_icon_path} {dest_png_path}")
        run_cmd(f"magick convert {src_icon_path} {dest_icns_path}")

    if args.prep_only:
        logger.info(f"App prepared successfully at {app_path}")
    else:
        run_cmd("npm install", cwd=app_path)
        run_cmd("npm run make", cwd=app_path)
        logger.info(f"App built successfully at {app_path / 'out'}")
