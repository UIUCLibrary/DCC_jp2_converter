from .abs_builder import AbsBuilder


class IgnoreExif(AbsBuilder):
    """Takes a tiff file source and ignores the any exif-metatdata."""

    def get_dst_args(self):
        self._imagemagick_command._dst_args = []

    def get_src_args(self):
        self._imagemagick_command._src_args = ['-define', 'tiff:exif-properties=false']

    def get_program_command(self):
        self._imagemagick_command._program = self.program_command
