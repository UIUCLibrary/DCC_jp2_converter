import typing
from collections import namedtuple
from typing import Iterator
import os
import warnings
CollectionPair = namedtuple("CollectionPair", ['tiff', 'jp2'])


def find_access_folders(path) -> Iterator[str]:
    """
    Search a given path recursively for access folders.

    Args:
        path: starting directory to search folders

    Yields:
        Paths to directories with the name "access"

    """
    warnings.warn("Use find_access_folders in the profile instead", DeprecationWarning)
    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            if _dir == "access":
                yield os.path.join(root, _dir)


def get_tiffs(path) -> Iterator[str]:
    """
    Search for tiff files in a given folder

    Args:
        path: Directory to search for tiff files

    Yields:
        Full path to a tiff file

    """
    for item in os.scandir(path):
        if os.path.splitext(item.name)[1].lower() != ".tif":
            continue
        yield item.path


def find_converted_pair(folder: str) -> typing.Iterator[CollectionPair]:
    """
    Search recursively from a path to find matching pairs of jp2 and tiff files with the same basename in the same
    folder.


    Args:
        folder: root directory to search from.

    Yields: Matches, if any.

    """
    for root, dirs, files in os.walk(folder):
        for file_ in files:
            if os.path.splitext(file_)[1].lower() == ".jp2":
                possible_tiff_match = os.path.splitext(file_)[0] + ".tif"
                if possible_tiff_match in files:
                    yield CollectionPair(tiff=os.path.join(root, possible_tiff_match), jp2=os.path.join(root, file_))
