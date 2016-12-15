import os
import ImagemagickDriver
from ImagemagickDriver.commandBuilders import DefaultCommandBuilder
from ImagemagickDriver.commandBuilders.abs_builder import AbsBuilder
from ImagemagickDriver.config import get_imagemagick_path

class Director:
    """Use this to generate commands for sending to imagemagick"""

    def __init__(self, builder: AbsBuilder = DefaultCommandBuilder(), program_path=get_imagemagick_path()):
        """
        Configure how the director should configure the builders. All args are for overriding the defaults.


        Args:
            builder: Choose which typo of command builder to user. By default, it uses the DefaultCommandBuilder.
            program_path: Override the location of imagemagick's convert utility.
        """
        self._builder = builder
        self._src = None
        self._dst = None

        # if program_path is None:
        #     program_path = shutil.which("convert")
        #     if program_path is None:
        #         raise FileNotFoundError(
        #             "Unable to find Convert program, make sure it's installed and on your system path")
        if not os.path.exists(program_path):
            raise FileNotFoundError("Unable to find {} program.".format(program_path))
        self._builder.set_program_command(program_path)

    def build_command(self, src: str, dst: str) -> list:
        """
        Builds an imagemagick command

        Args:
            src: Path to the source file
            dst: Path and file name to save a new file

        Returns:
            Returns a new command in list format.

        Examples:
            If no builder type is given as an argument to the Director, Imagemagick with infers the desired type based on the
            file extension of the destination file.


            >>> SOURCE_FILE_NAME = "/Users/hborcher/Documents/471223_037.tif"
            >>> DESTINATION_FILE_NAME = "/Users/hborcher/Documents/output.jpg"
            >>> command_builder = Director()
            >>> command_builder.build_command(src=SOURCE_FILE_NAME, dst=DESTINATION_FILE_NAME)
            ['/usr/local/bin/convert', '/Users/hborcher/Documents/471223_037.tif', '/Users/hborcher/Documents/output.jpg']

        """

        self._builder.new_command()
        self._builder.get_program_command()
        self._builder.set_src(src)
        self._builder.get_src_args()
        self._builder.set_dst(dst)
        self._builder.get_dst_args()
        return self._builder.get_command().command_list
