import abc
import typing


class AbsProfile(metaclass=abc.ABCMeta):
    path = ""

    @abc.abstractmethod
    def configure(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def convert_access_folder(self, path, destination=None):
        pass

    @staticmethod
    @abc.abstractmethod
    def find_access_folders(path)->typing.Iterator[str]:
        pass

