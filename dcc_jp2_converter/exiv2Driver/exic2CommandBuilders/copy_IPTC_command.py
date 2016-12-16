from .abs_builder import AbsBuilder


class CopyIPTCCommand(AbsBuilder):
    """Copies metadata from the source to the arg(destination file).

    The equivalent exiv2 command might look like this::

        exiv2 -it img1.jpg img2.jpg

    """

    def build_program_command(self):
        self._exiv_command.append(self.program_command)

    def build_option(self):
        self._exiv_command.append("-it")

    def build_arg(self, arg):
        self._exiv_command.append(arg)

    def set_src(self, filename):
        self._exiv_command.insert(-1, filename)
