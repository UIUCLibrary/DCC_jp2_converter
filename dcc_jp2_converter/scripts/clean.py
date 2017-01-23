import logging
import os
import stat
from dcc_jp2_converter import file_manager
logger = logging.getLogger("dcc_jp2_converter")


def cleanup_path(path: str):
    """
    Command for removing access tiffs that have a matching access jp2.
    Args:
        path: Path to clean.

    Note:
        The command, cleanup_path(), scans the path recursively.

    """
    logger.info("Deleting access tiffs found in \"{}\" that have already been converted into jp2 files.".format(path))

    total_files_removed = 0

    for tiff, jp2 in file_manager.find_converted_pair(path):
        # remove the read only attribute first
        os.chmod(tiff, stat.S_IWRITE)

        os.remove(tiff)
        logger.info("Deleted {}.".format(tiff))
        total_files_removed += 1

    logger.info("Finished cleaning.")
    logger.info("Deleted {} files.".format(total_files_removed))