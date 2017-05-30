from dcc_jp2_converter import Converter, file_manager
import logging
from dcc_jp2_converter.modules import profiles

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
    try:
        profile = profiles.get_profile(kwargs["profile"].lower())
    except KeyError as e:
        raise ValueError("Unknown profile {}.".format(e))
    profile.configure(overwrite=kwargs['overwrite'], remove_on_success=kwargs['remove'])
    for i, folder in enumerate(folders):
        logger.info(
            "Folder: {} of {}: \"{}\"".format(i + 1, len(folders), folder))

        # Do the work!
        profile.convert_access_folder(folder)
