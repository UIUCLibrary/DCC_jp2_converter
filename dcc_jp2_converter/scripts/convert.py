from dcc_jp2_converter import converter, file_manager
import logging

logger = logging.getLogger(__package__)


def convert_path(args):
    logger.info(
        "Searching \"{}\" for object folders with access tiffs.".format(
            args.path))

    folders = list(file_manager.find_access_folders(args.path))
    for i, folder in enumerate(folders):
        logger.info(
            "Folder: {} of {}: \"{}\"".format(i + 1, len(folders), folder))

        # Do the work!
        converter.convert_tiff_access_folder(
            folder,
            overwrite_existing=args.overwrite,
            remove_on_success=args.remove
        )