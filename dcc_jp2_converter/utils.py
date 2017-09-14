from __future__ import print_function
import pkg_resources
import abc
import os

import sys


class AbsConfigSearcherStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self) -> str:
        pass


class ConfigSearcherPkgResourceStrategy(AbsConfigSearcherStrategy):
    """
    Searches pkg_resources resources for the file
    """

    def find(self):
        try:
            requirement = pkg_resources.Requirement.parse("DCC_jp2_converter")
            return pkg_resources.resource_filename(requirement, "settings/command_paths.ini")
        except pkg_resources.DistributionNotFound:
            raise FileNotFoundError


class ConfigSearcherHomeDirectory(AbsConfigSearcherStrategy):
    """
    Searches Home folder for the config file.
    """

    def find(self) -> str:
        home_overwrites = os.path.join(os.path.expanduser("~"), "command_paths.ini")

        if os.path.exists(home_overwrites):
            return home_overwrites
        else:
            raise FileNotFoundError


class ConfigSearcherBundled(AbsConfigSearcherStrategy):
    """
    Searches the root folder for the command_paths file
    """

    def find(self) -> str:
        if getattr(sys, 'frozen', False):
            datadir = os.path.dirname(sys.executable)
        else:
            datadir = os.path.abspath(os.path.dirname(__file__))

        bundled_config = os.path.join(datadir, "command_paths.ini")

        if os.path.exists(bundled_config):
            return bundled_config
        else:
            raise FileNotFoundError


class ConfigSearcher:
    def __init__(self, strategy: AbsConfigSearcherStrategy) -> None:
        self._strategy = strategy

    def locate_config(self):
        return self._strategy.find()


def get_config_files():
    config_files = []
    search_strategies = [
        ConfigSearcherPkgResourceStrategy,
        ConfigSearcherBundled,
        ConfigSearcherHomeDirectory,

    ]

    for strategy in search_strategies:
        searcher = ConfigSearcher(strategy())
        try:
            result = searcher.locate_config()
            config_files.append(result)
        except FileNotFoundError:
            pass

    if config_files:
        return config_files
    raise FileNotFoundError("No config files found")
