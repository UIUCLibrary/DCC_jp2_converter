import os


class KakaduCommandBuilder:
    def __init__(self, builder, program_path):
        self.program_path = program_path
        self._builder = builder

        if not os.path.exists(program_path):
            raise FileNotFoundError(
                "Unable to find {} program.".format(program_path))

    def build_command(self, src: str, dst: str) -> list:
        self._builder.new_command()
        self._builder.set_src(src)
        self._builder.set_dst(dst)
        self._builder.set_args()
        return self._builder.get_command()