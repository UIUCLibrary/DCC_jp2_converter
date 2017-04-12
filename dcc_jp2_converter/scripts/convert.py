from dcc_jp2_converter import converters, file_manager
import logging

logger = logging.getLogger(__package__)


def convert_path(path: str, **kwargs):
    """
    High level. Run conversion.

    Args:
        path: Path to find items to search for directories and convert them

    """
    logger.info(
        "Searching \"{}\" for object folders with access tiffs.".format(
            path))

    folders = list(file_manager.find_access_folders(path))
    for i, folder in enumerate(folders):
        logger.info(
            "Folder: {} of {}: \"{}\"".format(i + 1, len(folders), folder))

        # Do the work!
        converter = converters.get_converter("ImageMagick")
        converter.convert_tiff_access_folder(
            path=folder,
            overwrite_existing=kwargs['overwrite'],
            remove_on_success=kwargs['remove']
        )
