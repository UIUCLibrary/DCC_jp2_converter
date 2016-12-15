import os
import shutil

from ImagemagickDriver.commandBuilders.abs_builder import AbsBuilder


class DefaultCommandBuilder(AbsBuilder):
    """Default command builder. Passes no arguments to Imagemagick so imagemagick infers the output based on the
    file extension.

    """

    def get_dst_args(self):
        self._imagemagick_command._dst_args = []

    def get_src_args(self):
        self._imagemagick_command._src_args = []

    def get_program_command(self):
        self._imagemagick_command._program = self.program_command


