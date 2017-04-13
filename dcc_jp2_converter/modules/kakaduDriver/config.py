import configparser
import shutil

from dcc_jp2_converter.modules.utils import get_config_files


def get_kdu_compress_path():
    """
    Attempts to retrieve the location to kakadu_compress command. If a path is
     specified in the settings ini file, that path will be used. Otherwise,
     the function will search for it on the path.

    Returns:
        Full path to exiv2 command if found.

    """
    config = configparser.ConfigParser()
    try:
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('kdu_compress', shutil.which("kdu_compress"))
    except KeyError:
        return shutil.which("kdu_compress")
