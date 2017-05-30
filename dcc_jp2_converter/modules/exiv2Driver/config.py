import configparser
import shutil
from dcc_jp2_converter.modules import abs_driver_config
from dcc_jp2_converter.modules.utils import get_config_files
import dcc_jp2_converter.thirdparty
import os
import warnings
import logging

class Exiv2Path(abs_driver_config.AbsDriverConfig):
    @staticmethod
    def check_config():
        config = configparser.ConfigParser()
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('exiv2')

    @staticmethod
    def driver_name() -> str:
        return "exiv2"

    @staticmethod
    def check_path():
        return shutil.which("exiv2")

    @staticmethod
    def check_bundled():
        third_party_path = dcc_jp2_converter.thirdparty.__path__[0]
        kdu_compress_path = os.path.join(third_party_path, "exiv2")
        return shutil.which("exiv2", path=kdu_compress_path)

    def get_path(self):
        logger = logging.getLogger(__name__)
        path = super().get_path()
        logger.debug("Using {} for {}".format(path, self.driver_name()))
        return path



def get_exiv2_path():
    """
    Attempts to retrieve the location to exiv2 command. If a path is
     specified in the settings ini file, that path will be used. Otherwise,
     the function will search for it on the path.

    Returns:
        Full path to exiv2 command if found.

    """
    warnings.warn("get_exiv2_path is deprecated. Use Exiv2Path class instead", DeprecationWarning)
    config = configparser.ConfigParser()
    try:
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('exiv2', shutil.which("exiv2"))
    except KeyError:
        return shutil.which("exiv2")
