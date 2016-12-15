import shutil

from ImagemagickDriver.commandBuilders.abs_builder import AbsBuilder


class Jp2AccessCommandBuilder(AbsBuilder):
    """
    Command builder for making access JPEG2000 .jp2 files for medusa.
    """

    def get_dst_args(self):
        self._imagemagick_command._dst_args = []

    def get_src_args(self):
        self._imagemagick_command._src_args = []

    def get_program_command(self):
        self._imagemagick_command._program = Jp2AccessCommandBuilder.program_command
