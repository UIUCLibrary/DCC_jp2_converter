import configparser
import shutil

from dcc_jp2_converter.modules.utils import get_config_files


def get_imagemagick_path():
    """
    Attempts to retrieve the location to Imagemagick convert command. If a
     path is specified in the settings ini file, that path will be used.
     Otherwise, the function will search for it on the path.

    Returns:
        Full path to Imagemagick convert command if found.

    """
    config = configparser.ConfigParser()
    try:
        for config_file in get_config_files():
            config.read(config_file)
        return config['commands'].get('convert', shutil.which("convert"))

    except KeyError:
        imgmagick_path = shutil.which("convert")
    return imgmagick_path
