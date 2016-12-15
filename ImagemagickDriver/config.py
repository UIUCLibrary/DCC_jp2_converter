import configparser
import shutil


def get_imagemagick_path():
    config = configparser.ConfigParser()
    config.read("settings/settings.ini")
    return config['commands'].get('convert', shutil.which("convert"))


# try:
# except KeyError:
#     EXIV2_PATH = shutil.which("exiv2")
