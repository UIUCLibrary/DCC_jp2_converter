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
from .modules import converter

__version__ = "0.0.3b3"
__all__ = ['modules']
