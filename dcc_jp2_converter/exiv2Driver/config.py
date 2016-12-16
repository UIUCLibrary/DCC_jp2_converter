import configparser
import shutil


def get_exiv2_path():
    """
    Attempts to retrieve the location to exiv2 command. If a path is specified in the settings ini file, that path will
    be used. Otherwise, the function will search for it on the path.

    Returns:
        Full path to exiv2 command if found.

    """
    config = configparser.ConfigParser()
    try:
        config.read("settings/settings.ini")
        return config['commands'].get('exiv2', shutil.which("exiv2"))
    except KeyError:
        return shutil.which("exiv2")