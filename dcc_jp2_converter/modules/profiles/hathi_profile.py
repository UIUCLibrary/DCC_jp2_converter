import os

from dcc_jp2_converter.modules.profiles.profile import AbsProfile
import logging
from dcc_jp2_converter import Converter
import typing


class HathiBase(AbsProfile):
    @staticmethod
    def find_access_folders(path) -> typing.Iterator[str]:
        raise NotImplementedError

    converter = Converter.create("Kakadu")
    remove_on_success = False
    overwrite = False
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

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
        self.logger.debug("Converting access folder of {} with the HathiProfile".format(path))
        self.converter.convert_tiff_access_folder2(
            source=path,
            destination=destination,
            overwrite_existing=self.overwrite,
            remove_on_success=self.remove_on_success
        )


class HathiProfile(HathiBase):

    @staticmethod
    def find_access_folders(path)->typing.Iterator[str]:
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


class HathiFlatProfile(HathiProfile):

    @staticmethod
    def find_access_folders(path) -> typing.Iterator[str]:
        def has_tiff_files(sub_path):
            for file in os.scandir(sub_path):
                if os.path.splitext(file.name)[1] == ".tif":
                    return True
            else:
                return False

        for directory in filter(lambda i: i.is_dir(), os.scandir(path)):
            if has_tiff_files(directory):
                yield directory.path
