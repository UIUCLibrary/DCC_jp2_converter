import os

from .exic2CommandBuilders.abs_builder import AbsBuilder
from .config import get_exiv2_path


class Exiv2CommandBuilder:
    """Use this to generate commands for sending to exiv2. """

    def __init__(self, builder: AbsBuilder, program_path=get_exiv2_path()):
        """Configure how the director should configure the builders.

        Args:
            builder: Choose which type of command to build.
            program_path: Override the location of exiv2 utility.
        """
        self._builder = builder
        self._src = None

        if not os.path.exists(program_path):
            raise FileNotFoundError("Unable to find {} program.".format(program_path))
        self._builder.set_program_command(program_path)

    def build_command(self, src: str, arg: str = None) -> list:
        """
        Builds an exiv2 command

        Args:
            src: Path to the source file
            arg: (Optional) Additional argument to the command.

        Returns:
            Returns a new command in list format.

        Examples:
            Example 1: Extracts IPTC datasets of a tiff file into an XMP sidecar

            >>> from dcc_jp2_converter.exiv2Driver import exic2CommandBuilders
            >>> SOURCE_FILE_NAME = "/Documents/471223_037.tif"
            >>> command_builder = Exiv2CommandBuilder(builder=exic2CommandBuilders.ExtractIPTCCommand())
            >>> command_builder.build_command(src=SOURCE_FILE_NAME)
            ['/usr/local/bin/exiv2', '-eiX', '/Documents/471223_037.tif

            Example 2: Copy Metadata from a tiff file to a jp2 file

            >>> from dcc_jp2_converter.exiv2Driver import exic2CommandBuilders
            >>> SOURCE_FILE_NAME = "/Documents/471223_037.tif"
            >>> DESTINATION_FILE_NAME = "/Documents/471223_037.jp2"
            >>> command_builder = Exiv2CommandBuilder(builder=exic2CommandBuilders.CopyIPTCCommand())
            >>> command_builder.build_command(src=SOURCE_FILE_NAME, arg=DESTINATION_FILE_NAME)
            ['/usr/local/bin/exiv2', '-it', '/Documents/471223_037.tif', '/Documents/471223_037.jp2']

        """

        self._builder.new_command()
        self._builder.build_program_command()
        self._builder.build_option()
        self._builder.build_arg(arg)
        self._builder.set_src(src)
        return self._builder.get_command()
