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
            self.overwrite = kwargs['overwrite']
        if "remove_on_success" in kwargs:
            self.remove_on_success = kwargs['remove_on_success']

    def convert_access_folder(self, path):
        self.converter.convert_tiff_access_folder(
            path=path,
            overwrite_existing=self.overwrite,
            remove_on_success=self.remove_on_success
        )
