from .abs_builder import AbsBuilder


class ExtractIPTCCommand(AbsBuilder):
    """Extract all embedded into a XMP sidecar file with extension .xmp.

    The equivalent exiv2 command might look like this::

        exiv2 -eaX image.jpg

    """

    def build_program_command(self):
        self._exiv_command.append(self.program_command)
        pass

    def build_option(self):
        self._exiv_command.append("-eaX")
        pass

    def build_arg(self, arg):
        # There are no extra argument for extracting this data
        pass
