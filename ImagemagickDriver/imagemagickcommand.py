import os


class ImagemagickCommand:

    def __init__(self):
        self._src = None
        self._dst = None
        self._program = None
        self._src_args = []
        self._dst_args = []

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        if not os.path.exists(value):
            raise FileNotFoundError
        self._src = os.path.abspath(value)

    @property
    def dst(self):
        return self._dst

    @dst.setter
    def dst(self, value):
        self._dst = os.path.abspath(value)

    @property
    def command_list(self):
        new_command_list = [self._program]
        new_command_list += self._src_args
        new_command_list.append(self.src)
        new_command_list += self._dst_args
        new_command_list.append(self.dst)

        return new_command_list

    def __str__(self):
        return str(self.command_list)