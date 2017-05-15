"""
This module contains all the logic for managing and executing the task of
converting jp2 tiff files into jp2 images for the digital library.
"""
from .modules import file_manager
from .modules import exiv2Driver
from .modules.exiv2Driver import Exiv2CommandBuilder
from .modules.exiv2Driver import exiv2CommandBuilders
from .modules import ImagemagickDriver
from .modules.ImagemagickDriver import imagemagickCommandBuilders
from .modules.ImagemagickDriver import ImagemagickCommandBuilder
from .modules import kakaduDriver
from .modules.kakaduDriver import KakaduCommandBuilder
from .modules.kakaduDriver import kakaduCommandBuilders
from .modules.converters import Converter
__version__ = "0.1.1"
__all__ = ['modules']
