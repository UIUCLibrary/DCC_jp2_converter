import logging
import os
from dcc_jp2_converter.modules.file_manager import find_converted_pair
logger = logging.getLogger(__package__)


def cleanup_path(path: str):
    logger.info("Deleting access tiffs found in \"{}\" that have already been converted into jp2 files.".format(path))

    total_files_removed = 0

    for tiff, jp2 in find_converted_pair(path):
        os.remove(tiff)
        logger.info("Deleted {}.".format(tiff))
        total_files_removed += 1

    logger.info("Finished cleaning.")
    logger.info("Deleted {} files.".format(total_files_removed))