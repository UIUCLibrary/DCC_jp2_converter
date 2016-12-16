from typing import Iterator
import os


def find_access_folders(path) -> Iterator[str]:
    """
    Search a given path recursively for access folders.

    Args:
        path: starting directory to search folders

    Yields:
        Paths to directories with the name "access"

    """
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
