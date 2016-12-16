from .abs_builder import AbsBuilder


class InsertIPTCCommand(AbsBuilder):
    """Inserts IPTC and XMP metadata from an XMP sidecar file into an image.

    The equivalent exiv2 command might look like this::

        exiv2 -iixX image.jpg

    """

    def build_program_command(self):
        self._exiv_command.append(self.program_command)

    def build_option(self):
        self._exiv_command.append("-iixX")

    def build_arg(self, arg):
        # There are no extra argument for inserting the sidecar data
        pass
