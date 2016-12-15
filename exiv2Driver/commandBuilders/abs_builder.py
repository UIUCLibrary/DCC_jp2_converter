import abc


class AbsBuilder(metaclass=abc.ABCMeta):
    """Abstract base class. Extend this class to create additional builders"""

    @classmethod
    def set_program_command(cls, program_path):
        cls.program_command = program_path

    def get_command(self):
        return self._exiv_command

    def new_command(self):
        self._exiv_command = []

    def set_src(self, filename):
        self._exiv_command.append(filename)

    @abc.abstractmethod
    def build_program_command(self):
        """
        Abstract: Sets the full path to executable program, such as Imagemagicks's "convert" command.

        """

    @abc.abstractmethod
    def build_option(self):
        """
        Abstract: Sets any correct operating command for exiv2.

        """

    @abc.abstractmethod
    def build_arg(self, arg):
        """
        Abstract: Sets any correct additional argument for exiv2.

        """
