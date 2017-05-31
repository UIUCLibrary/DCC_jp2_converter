"""Command line interface for DCC jp2 Converter."""
import argparse
import configparser
import logging
import os
import sys
import traceback

import dcc_jp2_converter
from dcc_jp2_converter.logger_config import configure_logger
from dcc_jp2_converter.modules.profiles.utils import get_all_profiles
from dcc_jp2_converter.scripts import clean
from dcc_jp2_converter.scripts import convert
from dcc_jp2_converter.scripts import validation

# find_settings_errors, find_arg_errors

ERROR_LOGGING_FILE = "errors.log"
DEFAULT_LOG_FILE = "processing.log"


DESCRIPTION = "Script for creating JP2 files from tiffs for the Medusa Digital Library."


def print_banner():
    print(DESCRIPTION, flush=True)
    print("University of Illinois")
    print("Written by Henry Borchers")
    print("\n")
    print("Version: {}".format(dcc_jp2_converter.__version__))
    print("-" * len(DESCRIPTION))
    print("\n")


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
        config_files = dcc_jp2_converter.modules.get_config_files()
    except FileNotFoundError:
        print("No command_paths.ini config file found.", file=sys.stderr)
        raise

    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        usage='%(prog)s [path] [options]',
        epilog="Settings for this script can be configured at {}: ".format(
            config_files[-1]))

    parser.add_argument('path', help="Path to the submission package")
    profile_group = parser.add_mutually_exclusive_group()
    profile_group.add_argument(
        "--profile",
        default="default",
        help="Set the conversion profile preset")
    profile_group.add_argument(
        "--list_profiles",
        action="store_true",
        help="List available profiles"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=dcc_jp2_converter.__version__)

    parser.add_argument(
        '--overwrite',
        action="store_true",
        help="Overwrite any existing jp2 with new ones")

    post_work_group = parser.add_mutually_exclusive_group()
    post_work_group.add_argument(
        '--clean',
        action="store_true",
        help="Clean up folders by removing any access tiff that have already been converted into jp2")

    post_work_group.add_argument(
        '--remove',
        action="store_true",
        help="Removes access tiff files after converting them.")

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


def run():
    logger = logging.getLogger(__name__)
    # Get user args
    args = get_args()
    print_banner()

    if args.debug:
        print("Using DEBUG mode!")

    # Set up logging
    configure_logger(debug_mode=args.debug, log_file=args.logname)
    logger.debug("Validating command line arguments.")

    # Do error checking
    errors = validation.find_arg_errors(args)
    if errors:
        for error in errors:
            logger.error(error)
        error_msg = "Invalid arguments."
        logger.error(error_msg)
        raise ValueError("{}\n{}".format(error_msg, "\n".join(errors)))

    logger.debug("Command line arguments are valid.")
    # Fixme:
    # errors = validation.find_settings_errors()
    # if errors:
    #     for error in errors:
    #         logger.error(error)
    #     error_msg = "Invalid settings."
    #     logger.error(error_msg)
    #     raise ValueError("{}\n{}".format(error_msg, "\n".join(errors)))

    # Find all the folders that contain files that need to be converted

    try:
        if args.clean:
            clean.cleanup_path(args.path)
        elif args.list_profiles:
            profiles = get_all_profiles()
            print("Available profiles:")
            for profile in profiles:
                print("  {}".format(profile))

            print()


        else:
            command_args = vars(args).copy()
            del command_args['path']
            try:
                convert.convert_path(args.path, **command_args)
            except ValueError as e:
                logger.error("Error: {}".format(e))
            except FileNotFoundError as e:
                logger.error("Error: {}".format(e))

        # print("\n\nAll Done!\n")
    except KeyboardInterrupt:
        logger.warning("Job Terminated")
    print("Log file located at {}".format(os.path.abspath(args.logname)))


def main():
    if "DEVMODE" in os.environ:
        msg = "* WARNING: Development mode is current on! *"
        print("\n", file=sys.stderr, flush=True)
        print("=" * len(msg), file=sys.stderr)
        print(msg, file=sys.stderr)
        print("=" * len(msg), file=sys.stderr)
        print("\n", file=sys.stderr)
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
                f.write("File: {}\n".format(os.path.dirname(sys.argv[0])))

                f.write("Version: {}\n".format(dcc_jp2_converter.__version__))

                args = str(get_args())
                f.write("Args: {}\n\n".format(args))

                f.write("Stacktrace:\n")
                f.write(tb)

                print("Detailed info about this error was saved to \"{}\"".format(ERROR_LOGGING_FILE), file=sys.stderr)

        finally:
            print("Script terminated.", file=sys.stderr)

        # If using development mode, Don't catch the exception!1
        if "DEVMODE" in os.environ:
            raise

        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest

        sys.exit(pytest.main(sys.argv[2:]))
    else:
        main()

