import abc

from ImagemagickDriver.imagemagickcommand import ImagemagickCommand


class AbsBuilder(metaclass=abc.ABCMeta):
    """Abstract base class. Extend this class to create additional builders"""

    @classmethod
    def set_program_command(cls, program_path):
        cls.program_command = program_path

    def get_command(self):
        return self._imagemagick_command

    def new_command(self):
        self._imagemagick_command = ImagemagickCommand()


    def set_src(self, filename):
        self._imagemagick_command.src = filename

    def set_dst(self, filename):
        self._imagemagick_command.dst = filename

    @abc.abstractmethod
    def get_program_command(self):
        """
        Abstract: Sets the full path to executable program, such as Imagemagicks's "convert" command.

        """

    @abc.abstractmethod
    def get_src_args(self):
        """
        Abstract: Sets any commandline arguments for the source file.

        """
        pass

    @abc.abstractmethod
    def get_dst_args(self):
        """
        Abstract: Sets any command line arguments for the source file.

        """
