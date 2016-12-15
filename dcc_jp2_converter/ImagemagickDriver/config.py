import configparser
import shutil


def get_imagemagick_path():
    config = configparser.ConfigParser()
    try:
        config.read("settings/settings.ini")
        imgmagick_path = config['commands'].get('convert', shutil.which("convert"))
    except KeyError:
        imgmagick_path = shutil.which("convert")
    return imgmagick_path


# try:
# except KeyError:
#     EXIV2_PATH = shutil.which("exiv2")
