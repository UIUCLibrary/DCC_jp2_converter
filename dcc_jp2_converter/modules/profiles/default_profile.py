import os

from dcc_jp2_converter.modules.profiles import profile
import logging
from dcc_jp2_converter import Converter


class DefaultProfile(profile.AbsProfile):
    logger = logging.getLogger(__name__)
    overwrite = False
    remove_on_success = False
    converter = Converter.create("ImageMagick")

    def configure(self, *args, **kwargs):
        if "overwrite" in kwargs:
            if kwargs['overwrite'] is True:
                self.logger.debug("Configuring setting to overwrite existing files.")
            self.overwrite = kwargs['overwrite']
        if "remove_on_success" in kwargs:
            if kwargs['remove_on_success'] is True:
                self.logger.debug("Configuring setting to remove original file on success.")
            self.remove_on_success = kwargs['remove_on_success']

    def convert_access_folder(self, path, destination=None):
        destination = destination or path
        self.converter.convert_tiff_access_folder2(
            source=path,
            destination=destination,
            overwrite_existing=self.overwrite,
            remove_on_success=self.remove_on_success
        )

    @staticmethod
    def find_access_folders(path):
        for root, dirs, files in os.walk(path):
            for _dir in dirs:
                if _dir == "access":
                    yield os.path.join(root, _dir)
