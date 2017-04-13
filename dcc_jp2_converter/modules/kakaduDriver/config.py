import configparser
import os
import shutil

from dcc_jp2_converter.modules.utils import get_config_files
import dcc_jp2_converter.thirdparty


def get_kdu_compress_path():
    """
    Attempts to retrieve the location to kakadu_compress command. If a path is
     specified in the settings ini file, that path will be used. Otherwise,
     the function will search for it on the path.

    Returns:
        Full path to exiv2 command if found.

    """

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

        path = shutil.which("kdu_compress", path=dcc_jp2_converter.thirdparty.__path__[0])
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