import os

from dcc_jp2_converter.modules.kakaduDriver import config


class KakaduCommandBuilder:
    def __init__(self, builder, program_path=None):
        if program_path:
            self.program_path = program_path
        else:
            path_finder = config.KduCompressPath()
            try:
                self.program_path = path_finder.get_path()
            except FileNotFoundError:
                raise FileNotFoundError("kakdu compress not found")
            # program_path = config.get_kdu_compress_path()
        # self.program_path = program_path
        self._builder = builder

        # if not os.path.exists(program_path):
        #     raise FileNotFoundError(
        #         "Unable to find {} program.".format(program_path))

    def build_command(self, src: str, dst: str) -> list:
        self._builder.new_command()
        self._builder.set_executable_path(self.program_path)
        self._builder.set_src(src)
        self._builder.set_dst(dst)
        self._builder.set_args()
        return self._builder.get_command()
