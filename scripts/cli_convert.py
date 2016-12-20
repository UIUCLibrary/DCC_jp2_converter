"""Command line interface for DCC jp2 Converter."""

import logging
import os
import sys

import argparse

import dcc_jp2_converter
from dcc_jp2_converter import converter
from dcc_jp2_converter.logging import InfoFilter


DEFAULT_LOG_FILE = "processing.log"
logger = logging.getLogger(__package__)


def get_args():
    """
    Parses the command line arguments.

    Returns:
        Parsed command line arguments.

    """
    parser = argparse.ArgumentParser(
        description="Create JP2 files from tiffs for digital Library",
        epilog="Settings for this script can be configured at {}: ".format(
            dcc_jp2_converter.get_config_file()))

    parser.add_argument('path', help="Path to the submission package")

    parser.add_argument(
        '--overwrite',
        action="store_true",
        help="Overwrite any existing jp2 with new ones")

    parser.add_argument(
        '--logname',
        default=DEFAULT_LOG_FILE,
        help="Change the log name.")

    parser.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")

    args = parser.parse_args()

    return args


def find_arg_errors(args):
    """
    Perform error check on command line arguments passed in in args to see if
    they are logically valid and return any errors if any are found.
    """

    errors = []
    if not os.path.exists(args.path):
        errors.append("Unable to find directory, \"{}\"".format(args.path))
    if os.path.isfile(args.path):
        errors.append("\"{}\" is not a directory.".format(args.path))
    return errors


def configure_logger(debug_mode=False, log_file=None):
    """
    Configure the settings for the logger.

    Args:
        debug_mode: Set the package into debug more.
        log_file: If a file name is given, all information presented to the
         screen with be saved into that file.

    """

    logger.setLevel(logging.DEBUG)

    logging_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setLevel(logging.INFO)
    std_handler.addFilter(InfoFilter())

    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.WARNING)

    if log_file:
        fl_handler = logging.FileHandler(log_file)
        fl_handler.setLevel(logging.INFO)
        fl_handler.setFormatter(logging_formatter)
        logger.addHandler(fl_handler)
    if debug_mode:
        std_handler.setLevel(logging.DEBUG)

        std_handler.setFormatter(logging_formatter)
        err_handler.setFormatter(logging_formatter)

    logger.addHandler(std_handler)
    logger.addHandler(err_handler)


def main():

    args = get_args()
    if args.debug:
        print("Using DEBUG mode!")

    # TODO: Make logging optional
    configure_logger(debug_mode=args.debug, log_file=args.logname)
    logger.debug("Validating command line arguments.")
    errors = find_arg_errors(args)
    if errors:
        for error in errors:
            logger.error(error)
        logger.error("Script terminated due to invalid arguments.")
        exit(1)

    logger.debug("Command line arguments are valid.")
    logger.info(
        "Searching \"{}\" for object folders with access tiffs".format(
            args.path))

    folders = list(dcc_jp2_converter.find_access_folders(args.path))
    try:
        for i, folder in enumerate(folders):
            logger.info(
                "Item: {} of {}: \"{}\"".format(i + 1, len(folders), folder))
            converter.convert_tiff_access_folder(
                folder, overwrite_existing=args.overwrite)

        print("\n\nAll Done!\n")
    except KeyboardInterrupt:
        logger.warning("Job Terminated")
    print("Log file located at {}".format(os.path.abspath(DEFAULT_LOG_FILE)))


if __name__ == '__main__':
    main()
