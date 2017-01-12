"""Command line interface for DCC jp2 Converter."""

import logging
import os
import sys

import argparse

import dcc_jp2_converter
from dcc_jp2_converter import converter
from dcc_jp2_converter.ImagemagickDriver import get_imagemagick_path
from dcc_jp2_converter.exiv2Driver import get_exiv2_path
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
            dcc_jp2_converter.get_config_files()[-1]))

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


def is_executable(path):
    if sys.platform == "win32":
        if os.path.splitext(path)[1].lower() == ".exe":
            return True
        else:
            return False

    # Unix based
    else:
        return os.access(path, os.X_OK)


def find_settings_errors():
    """
    Looks for any configuration errors to make sure that the script can operate properly
    with the given settings by the default path lookup or any changes provided by a
    command_paths.ini file.

    Returns:
        Returns a list of error messages if any. Returns an empty list if found no errors.

    """
    errors = []
    missing_programs = []

    not_found_message = "The following required programs were not found: \"{}\". Please make sure they installed " \
                        "on the path or command_paths.ini file is configured to point to their location in your home " \
                        "folder."

    ########################
    # Imagemagick settings #
    ########################
    imagemagick_path = get_imagemagick_path()

    # check exists
    if imagemagick_path is None or not os.path.exists(imagemagick_path):
        missing_programs.append("Imagemagick's convert command")
    else:
        # Check if found Windows "convert FAL to NTFS command" by mistake and if the item is executable
        if "system32" in imagemagick_path.lower() or not is_executable(imagemagick_path):
            errors.append("Imagemagick's convert command, \"{}\",is invalid. Check command_paths.ini file.".format(imagemagick_path))

    ##################
    # exiv2 settings #
    ##################
    exiv2_path = get_exiv2_path()

    # check exists
    if exiv2_path is None or not os.path.exists(exiv2_path):
        missing_programs.append("exiv2")
    else:

        # check is executable
        if not is_executable(exiv2_path):
            errors.append("exiv2 command, \"{}\", is invalid. Check command_paths.ini file.".format(exiv2_path))
    if missing_programs:
        errors.append(not_found_message.format("\", \"".join(missing_programs)))

    return errors


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
        debug_mode: Set the package into debug mode.
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

    errors = find_settings_errors()
    if errors:
        for error in errors:
            logger.error(error)
        logger.error("Script terminated due to invalid settings.")
        exit(1)

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
