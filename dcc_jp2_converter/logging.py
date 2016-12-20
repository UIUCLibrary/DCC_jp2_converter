import logging


class InfoFilter(logging.Filter):
    """
    Filter anything higher than Info level
    """

    def filter(self, record):
        return record.levelno <= logging.INFO


