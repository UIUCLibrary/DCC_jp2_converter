import typing
import os
from collections import namedtuple

CollectionPair = namedtuple("CollectionPair", ['tiff', 'jp2'])


def find_converted_pair(folder: str) -> typing.Iterator[CollectionPair]:
    """
    Search recursively from a path to find matching pairs of jp2 and tiff files with the same basename in the same
    folder.


    Args:
        folder: root directory to search from.

    Yields: Matches if any.

    """
    for root, dirs, files in os.walk(folder):
        for file_ in files:
            if os.path.splitext(file_)[1].lower() == ".jp2":
                possible_tiff_match = os.path.splitext(file_)[0] + ".tif"
                if possible_tiff_match in files:
                    yield CollectionPair(tiff=os.path.join(root, possible_tiff_match), jp2=os.path.join(root, file_))

