"""
This module contains all the logic for managing and executing the task of
converting jp2 tiff files into jp2 images for the digital library.
"""
from .ImagemagickDriver import imagemagickCommandBuilders
from .ImagemagickDriver import ImagemagickCommandBuilder
from .exiv2Driver import exiv2CommandBuilders
from .exiv2Driver import Exiv2CommandBuilder
from .file_manager import find_access_folders, get_tiffs
from .utils import get_config_files

__version__ = "0.0.1b4"
