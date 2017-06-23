import os

from dcc_jp2_converter.modules.profiles.profile import AbsProfile
import logging
from dcc_jp2_converter import Converter


class HathiProfile(AbsProfile):
    logger = logging.getLogger(__name__)
    overwrite = False
    remove_on_success = False
    converter = Converter.create("Kakadu")

    def configure(self, *args, **kwargs):
        if "overwrite" in kwargs:
            if kwargs['overwrite'] is True:
                self.logger.debug("Configuring setting to overwrite existing files.")
            self.overwrite = kwargs['overwrite']
        if "remove_on_success" in kwargs:
            if kwargs['remove_on_success'] is True:
                self.logger.debug("Configuring setting to remove original file on success.")
            self.remove_on_success = kwargs['remove_on_success']

    def convert_access_folder(self, path):
        self.logger.debug("Converting access folder of {} with the HathiProfile".format(path))
        self.converter.convert_tiff_access_folder(
            path=path,
            overwrite_existing=self.overwrite,
            remove_on_success=self.remove_on_success
        )

    @staticmethod
    def find_access_folders(path)->str:
        """
        Searches the path recursively for a folder named "access" and yields every folder within that access folder.

        Args:
            path: starting directory to search folders

        Yields:
            Paths to directories with the name "access"
        """

        def find_root_access():
            for root, dirs, files in os.walk(path):
                for _dir in dirs:
                    if _dir == "access":
                        yield os.path.join(root, _dir)

        for root_access in find_root_access():
            for access_folder in filter(lambda x: os.path.isdir(x), os.scandir(root_access)):
                yield access_folder.path
