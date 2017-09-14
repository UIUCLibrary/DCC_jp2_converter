import os

from .exiv2CommandBuilders.abs_builder import AbsBuilder
# from .config import get_exiv2_path
from dcc_jp2_converter.modules.exiv2Driver import config


class Exiv2CommandBuilder:
    """Use this to generate commands for sending to exiv2. """

    def __init__(
            self, builder: AbsBuilder, program_path=None) -> None:
        """Configure how the director should configure the builders.

        Args:
            builder: Choose which type of command to build.
            program_path: Override the location of exiv2 utility.
        """
        if not program_path:
            path_finder = config.Exiv2Path()
            try:
                program_path = path_finder.get_path()
                assert os.path.exists(program_path)
            except FileNotFoundError:
                raise FileNotFoundError("exiv2 not found")

        self._builder = builder
        self._src = None

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
            Extract metadata:

                .. code-block:: python

                    # Extract all metadata of a tiff file into an XMP sidecar file.

                    from dcc_jp2_converter import exiv2CommandBuilders
                    from dcc_jp2_converter import Exiv2CommandBuilder

                    SOURCE_FILE_NAME = "/Documents/471223_037.tif"

                    command_builder = Exiv2CommandBuilder(builder=exiv2CommandBuilders.ExtractIPTCCommand())
                    command_builder.build_command(src=SOURCE_FILE_NAME)


                    # This returns the following value
                    # ['/usr/local/bin/exiv2','-eaX', '/Documents/471223_037.tif']

            Copy Metadata:

                .. code-block:: python

                    # Copy Metadata from a tiff file to a jpg file

                    from dcc_jp2_converter import exiv2CommandBuilders
                    from dcc_jp2_converter import Exiv2CommandBuilder

                    SOURCE_FILE_NAME = "/Documents/471223_037.tif"
                    DESTINATION_FILE_NAME = "/Documents/471223_037.jpg"

                    command_builder = Exiv2CommandBuilder(builder=exiv2CommandBuilders.CopyIPTCCommand())
                    command_builder.build_command(src=SOURCE_FILE_NAME, arg=DESTINATION_FILE_NAME)

                    # This returns the following value
                    ['/usr/local/bin/exiv2', '-it', '/Documents/471223_037.tif', '/Documents/471223_037.jpg']

        """

        self._builder.new_command()
        self._builder.build_program_command()
        self._builder.build_option()
        self._builder.build_arg(arg)
        self._builder.set_src(src)
        return self._builder.get_command()
