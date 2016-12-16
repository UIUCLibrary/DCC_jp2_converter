import logging
import sys
from dcc_jp2_converter import logger


class InfoFilter(logging.Filter):
    """
    Filter anything higher than Info level
    """
    def filter(self, record):
        return record.levelno <= logging.INFO


def configure_logger(debug_mode=False, log_file=None):
    logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
