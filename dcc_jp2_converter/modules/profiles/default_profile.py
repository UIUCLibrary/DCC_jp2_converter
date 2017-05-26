from dcc_jp2_converter.modules.profiles.profile import AbsProfile
import logging
from dcc_jp2_converter import Converter


class DefaultProfile(AbsProfile):
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

    def convert_access_folder(self, path):
        self.converter.convert_tiff_access_folder(
            path=path,
            overwrite_existing=self.overwrite,
            remove_on_success=self.remove_on_success
        )
