import logging
import sys

from dcc_jp2_converter.scripts import logging_settings


def configure_logger(debug_mode=False, log_file=None):
    logger = logging.getLogger(__package__)

    """
    Configure the settings for the logger.

    Args:
        debug_mode: Set the package into debug mode.
        log_file: If a file name is given, all information presented to the
         screen with be saved into that file.

    """

    logger.setLevel(logging.DEBUG)

    friendly_format = logging.Formatter('%(asctime)s: %(message)s', datefmt='%I:%M:%S %p')
    debug_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setLevel(logging.INFO)
    std_handler.addFilter(logging_settings.InfoFilter())

    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.WARNING)

    if log_file:
        fl_handler = logging.FileHandler(log_file)
        fl_handler.setLevel(logging.INFO)
        fl_handler.setFormatter(debug_format)
        logger.addHandler(fl_handler)
    if debug_mode:
        std_handler.setLevel(logging.DEBUG)

        std_handler.setFormatter(debug_format)
        err_handler.setFormatter(debug_format)
    else:
        err_handler.setFormatter(friendly_format)
        std_handler.setFormatter(friendly_format)

    logger.addHandler(std_handler)
    logger.addHandler(err_handler)
