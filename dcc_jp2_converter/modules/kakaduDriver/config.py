import configparser
import os
import shutil

import logging

from dcc_jp2_converter.utils import get_config_files
import dcc_jp2_converter.thirdparty
from dcc_jp2_converter.modules import abs_driver_config
import warnings


class KduCompressPath(abs_driver_config.AbsDriverConfig):
    """
    Attempts to retrieve the location to kakadu_compress command. If a path is
     specified in the settings ini file, that path will be used. Otherwise,
     the function will search for it on the path.

    Returns:
        Full path to kdu command if found.

    """
    @staticmethod
    def check_config():
        config = configparser.ConfigParser()
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('kdu_compress')

    @staticmethod
    def driver_name() -> str:
        return "kdu_compress"

    @staticmethod
    def check_path():
        return shutil.which("kdu_compress")

    @staticmethod
    def check_bundled():
        third_party_path = dcc_jp2_converter.thirdparty.__path__[0]
        kdu_compress_path = os.path.join(third_party_path, "kdu_compress")
        return shutil.which("kdu_compress", path=kdu_compress_path)

    def get_path(self):
        logger = logging.getLogger(__name__)
        path = super().get_path()
        logger.debug("Using {} for {}".format(path, self.driver_name()))
        return path


def get_kdu_compress_path():
    """
    Attempts to retrieve the location to kakadu_compress command. If a path is
     specified in the settings ini file, that path will be used. Otherwise,
     the function will search for it on the path.

    Returns:
        Full path to exiv2 command if found.

    """
    warnings.warn("get_kdu_compress_path is deprecated. Use KduCompressPath class instead", DeprecationWarning)

    def check_config():
        config = configparser.ConfigParser()
        try:
            for config_file in get_config_files():
                config.read(config_file)
            command = config['commands']['kdu_compress']
            if not os.path.exists(command):
                raise FileNotFoundError
            return command
        except KeyError:
            raise FileNotFoundError

    def check_bundled():
        third_party_path = dcc_jp2_converter.thirdparty.__path__[0]
        kdu_compress_path = os.path.join(third_party_path, "kdu_compress")
        path = shutil.which("kdu_compress", path=kdu_compress_path)
        if path:
            return path
        else:
            raise FileNotFoundError

    def check_path():
        path = shutil.which("kdu_compress")
        if path:
            return path
        else:
            raise FileNotFoundError

    # =================================================
    # Check the location in the config file setting
    try:
        return check_config()
    except FileNotFoundError:
        pass

    # Check the for a config file setting
    try:
        return check_bundled()
    except FileNotFoundError:
        pass

    # If all else fails, check the path
    return check_path()
