import abc

from dcc_jp2_converter import kakaduDriver


class AbsBuilder(metaclass=abc.ABCMeta):
    def new_command(self):
        self._kakadu_command = [kakaduDriver.get_kdu_compress_path()]

    def set_src(self, src):
        self._kakadu_command.append("-i")
        self._kakadu_command.append(src)

    def set_dst(self, dst):
        self._kakadu_command.append("-o")
        self._kakadu_command.append(dst)

    @abc.abstractmethod
    def set_args(self):
        pass

    def get_command(self):
        return self._kakadu_command


class Simple(AbsBuilder):
    def set_args(self):
        pass


class HathiPreset(AbsBuilder):
    def set_args(self):

        self._kakadu_command.append("Clevels=5")
        self._kakadu_command.append("Clayers=8")
        self._kakadu_command.append("Corder=RLCP")
        self._kakadu_command.append("Cuse_sop=yes")
        self._kakadu_command.append("Cuse_eph=yes")
        self._kakadu_command.append("'Cmodes=RESET|RESTART|CAUSAL|ERTERM|SEGMARK'")
        self._kakadu_command.append("-no_weights")
        self._kakadu_command.append("-slope")
        self._kakadu_command.append("42988")