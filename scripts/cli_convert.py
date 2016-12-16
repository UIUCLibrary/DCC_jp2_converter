import os

import dcc_jp2_converter
import argparse
from dcc_jp2_converter import utils
from dcc_jp2_converter import logger
from dcc_jp2_converter import converter


def get_args():
    parser = argparse.ArgumentParser(description="Create JP2 files from tiffs for digital Library")
    parser.add_argument('path', help="Path to the submission package")
    parser.add_argument('--debug', action="store_true", help="Run script in debug mode")
    args = parser.parse_args()
    return args


def find_arg_errors(args):
    errors = []
    if not os.path.exists(args.path):
        errors.append("Unable to find directory, \"{}\"".format(args.path))
    if os.path.isfile(args.path):
        errors.append("\"{}\" is not a directory.".format(args.path))
    return errors


def main():
    args = get_args()
    if args.debug:
        print("Using DEBUG mode!")

    # TODO: Make logging optional
    utils.configure_logger(debug_mode=args.debug, log_file="/Users/hborcher/PycharmProjects/DCC_jp2_converter/mylog.log")

    logger.debug("Validating command line arguments.")
    errors = find_arg_errors(args)
    if errors:
        for error in errors:
            logger.error(error)
        logger.error("Script terminated due to invalid arguments.")
        exit(1)

    logger.debug("Command line arguments are valid.")
    logger.info("Searching \"{}\" for object folders with access tiffs".format(args.path))

    folders = list(dcc_jp2_converter.find_access_folders(args.path))
    for i, folder in enumerate(folders):
        logger.info("{} of {}: \"{}\"".format(i+1, len(folders), folder))
        converter.convert_tiff_access_folder(folder)







if __name__ == '__main__':

    main()
