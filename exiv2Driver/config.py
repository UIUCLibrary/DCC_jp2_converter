import configparser
import shutil


def get_exiv2_path():
    config = configparser.ConfigParser()
    config.read("settings/settings.ini")
    return config['commands'].get('exiv2', shutil.which("exiv2"))
