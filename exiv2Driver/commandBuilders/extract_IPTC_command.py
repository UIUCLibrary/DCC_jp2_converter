from exiv2Driver.commandBuilders.abs_builder import AbsBuilder


class ExtractIPTCCommand(AbsBuilder):
    """Extract IPTC dataset into a XMP sidecar file with extension .xmp"""

    def build_program_command(self):
        self._exiv_command.append(self.program_command)
        pass

    def build_option(self):
        self._exiv_command.append("-eiX")
        pass

    def build_arg(self, arg):
        # There are no extra argument for extracting this data
        pass
