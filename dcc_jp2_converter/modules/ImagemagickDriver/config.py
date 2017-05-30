import configparser
import shutil
import warnings

import logging

from dcc_jp2_converter.modules.utils import get_config_files
from dcc_jp2_converter.modules import abs_driver_config
import dcc_jp2_converter.thirdparty
import os


class ImagemagickPath(abs_driver_config.AbsDriverConfig):
    @staticmethod
    def check_config():
        config = configparser.ConfigParser()
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('convert')

    @staticmethod
    def driver_name() -> str:
        return "convert"

    @staticmethod
    def check_path():
        return shutil.which("convert")

    @staticmethod
    def check_bundled():
        third_party_path = dcc_jp2_converter.thirdparty.__path__[0]
        kdu_compress_path = os.path.join(third_party_path, "Imagemagick")
        return shutil.which("convert", path=kdu_compress_path)

    def get_path(self):
        logger = logging.getLogger(__name__)
        path = super().get_path()
        logger.debug("Using {} for {}".format(path, self.driver_name()))
        return path



def get_imagemagick_path():
    """
    Attempts to retrieve the location to Imagemagick convert command. If a
     path is specified in the settings ini file, that path will be used.
     Otherwise, the function will search for it on the path.

    Returns:
        Full path to Imagemagick convert command if found.

    """
    warnings.warn("get_imagemagick_path() is deprecated. Use ImagemagickPath class instead", DeprecationWarning)
    config = configparser.ConfigParser()
    try:
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('convert', shutil.which("convert"))

    except KeyError:
        imgmagick_path = shutil.which("convert")
    return imgmagick_path
