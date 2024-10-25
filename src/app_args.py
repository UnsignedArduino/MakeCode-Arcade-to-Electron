import logging
from argparse import ArgumentParser

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def add_app_args(parser: ArgumentParser):
    parser.add_argument("--repo", "-r", required=True, type=str,
                        help="The path to the MakeCode Arcade game repository on GitHub. "
                             "For example, \"UnsignedArduino/Racers\" points to "
                             "https://github.com/UnsignedArduino/Racers.")
    parser.add_argument("--version", "-v", required=True, type=str,
                        help="The version of the MakeCode Arcade game to convert. Must be "
                             "an already existing and working built version on GitHub "
                             "Pages. For example, \"1.0.0\". (do not include the \"v\" "
                             "prefix)")
    parser.add_argument("--name", "-n", required=True, type=str,
                        help="The name of the game. This will be the name of the Electron "
                             "app. For example, \"Racers\".")
    parser.add_argument("--author", "-a", required=True, type=str,
                        help="The author of the game. For example, \"Cyrus Yiu\".")
    parser.add_argument("--description", "-d", required=True, type=str,
                        help="The description of the game. For example, \"Enjoy the "
                             "high-speed thrills of car racing in MakeCode Arcade! For "
                             "the MakeCode Arcade Mini Game Jam #3.\".")
    parser.add_argument("--debug", action="store_const",
                        const=logging.DEBUG, default=logging.INFO,
                        help="Include debug messages. Defaults to info and "
                             "greater severity messages only.")
