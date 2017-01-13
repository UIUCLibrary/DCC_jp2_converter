"""Command line interface for DCC jp2 Converter."""
import argparse
import configparser
import logging
import os
import sys
import traceback

import dcc_jp2_converter
from dcc_jp2_converter import converter
from dcc_jp2_converter.logging import InfoFilter
from scripts.validation import find_settings_errors, find_arg_errors

ERROR_LOGGING_FILE = "errors.log"
DEFAULT_LOG_FILE = "processing.log"
logger = logging.getLogger(__package__)


def get_logging_name(config_files):
    config = configparser.ConfigParser()
    try:
        for config_file in config_files:
            config.read(config_file)
        return config['logging'].get('logname', DEFAULT_LOG_FILE)
    except KeyError:
        return DEFAULT_LOG_FILE


def get_args():
    """
    Parses the command line arguments.

    Returns:
        Parsed command line arguments.

    """
    try:
        config_files = dcc_jp2_converter.get_config_files()
    except FileNotFoundError:
        print("No command_paths.ini config file found.", file=sys.stderr)
        raise

    parser = argparse.ArgumentParser(
        description="Create JP2 files from tiffs for digital Library",
        usage='%(prog)s path [options]',
        epilog="Settings for this script can be configured at {}: ".format(
            config_files[-1]))

    parser.add_argument('path', help="Path to the submission package")

    parser.add_argument(
        '--version',
        action='version',
        version=dcc_jp2_converter.__version__)

    parser.add_argument(
        '--overwrite',
        action="store_true",
        help="Overwrite any existing jp2 with new ones")


    parser.add_argument(
        '--logname',
        default=get_logging_name(config_files),
        help="Change the log name.")

    parser.add_argument(
        '--debug',
        action="store_true",
        help="Run script in debug mode")

    args = parser.parse_args()

    return args


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


def run():

    # Get user args
    args = get_args()

    if args.debug:
        print("Using DEBUG mode!")

    # Set up logging
    configure_logger(debug_mode=args.debug, log_file=args.logname)
    logger.debug("Validating command line arguments.")

    # Do error checking
    errors = find_arg_errors(args)
    if errors:
        for error in errors:
            logger.error(error)
        error_msg = "Invalid arguments."
        logger.error(error_msg)
        raise ValueError("{}\n{}".format(error_msg, "\n".join(errors)))

    logger.debug("Command line arguments are valid.")
    logger.info(
        "Searching \"{}\" for object folders with access tiffs".format(
            args.path))

    errors = find_settings_errors()
    if errors:
        for error in errors:
            logger.error(error)
        error_msg = "Invalid settings."
        logger.error(error_msg)
        raise ValueError("{}\n{}".format(error_msg, "\n".join(errors)))

    # Find all the folders that contain files that need to be converted
    folders = list(dcc_jp2_converter.find_access_folders(args.path))

    try:
        for i, folder in enumerate(folders):
            logger.info(
                "Item: {} of {}: \"{}\"".format(i + 1, len(folders), folder))

            # Do the work!
            converter.convert_tiff_access_folder(
                folder, overwrite_existing=args.overwrite)

        print("\n\nAll Done!\n")
    except KeyboardInterrupt:
        logger.warning("Job Terminated")
    print("Log file located at {}".format(os.path.abspath(args.logname)))


def main():
    try:
        run()

    except KeyboardInterrupt:
        print("Exiting")

    except Exception as e:
        print("\n==============================", file=sys.stderr)
        print("Script failed due to an error.", file=sys.stderr)
        tb = traceback.format_exc()
        print("Reason: {}".format(e), file=sys.stderr)

        try:
            with open(ERROR_LOGGING_FILE, "w", encoding="utf8") as f:
                f.write("File: {}\n".format(__file__))

                f.write("Version: {}\n".format(dcc_jp2_converter.__version__))

                args = str(get_args())
                f.write("Args: {}\n\n".format(args))

                f.write("Stacktrace:\n")
                f.write(tb)

                print("Detailed info about this error was saved to \"{}\"".format(ERROR_LOGGING_FILE), file=sys.stderr)
        finally:
            print("Script terminated.", file=sys.stderr)

        exit(1)

if __name__ == '__main__':
    main()
