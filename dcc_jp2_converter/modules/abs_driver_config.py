import abc
import os


class AbsDriverConfig(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def check_config():
        pass

    @staticmethod
    @abc.abstractmethod
    def check_bundled():
        pass

    @staticmethod
    @abc.abstractmethod
    def check_path():
        pass

    @staticmethod
    @abc.abstractmethod
    def driver_name()->str:
        pass

    def search_order(self)->list:
        return [
            self.check_config,
            self.check_bundled,
            self.check_path
        ]

    def get_path(self):
        for path_search in self.search_order():
            path = path_search()
            if os.path.exists(path):
                return path

        raise FileNotFoundError("Unable to locate {}".format(self.driver_name))

