from exiv2Driver.commandBuilders.abs_builder import AbsBuilder


class CopyIPTCCommand(AbsBuilder):
    """Copies metadata from the source to the arg(destination file) """

    def build_program_command(self):
        self._exiv_command.append(self.program_command)

    def build_option(self):
        self._exiv_command.append("-it")

    def build_arg(self, arg):
        self._exiv_command.append(arg)

    def set_src(self, filename):
        self._exiv_command.insert(-1, filename)
