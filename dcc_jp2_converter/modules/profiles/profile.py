import abc


class AbsProfile(metaclass=abc.ABCMeta):
    path = ""

    @abc.abstractmethod
    def configure(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def convert_access_folder(self, path):
        pass
