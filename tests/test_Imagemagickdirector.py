import os
import sys

import pytest

from dcc_jp2_converter import imagemagick_command_builders as builders
from dcc_jp2_converter import imagemagick_driver as driver

if sys.platform == "win32":
    IMAGEMAGICK = "C:\\Program Files\\ImageMagick-6\\bin\convert.exe"
else:
    IMAGEMAGICK = "/usr/bin/convert"

@pytest.fixture
def default_builder(monkeypatch):
    """
    Test to make sure that a default command is generated in the case no
    other preset builder is made

    """


    # Because the location of imagemagick is faked for this example,
    # we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command = driver.ImagemagickCommandBuilder(program_path=IMAGEMAGICK)
    return command


def test_default_builder_tiff2jpg(default_builder):
    if sys.platform == "win32":
        src_file = "E:\\mysource\\sample.tif"
        dst_file = "E:\\mysource\\output.jpg"

    else:
        src_file = "/Users/Documents/sample.tif"
        dst_file = "/Users/Documents/output.jpg"

    command = default_builder.build_command(src=src_file, dst=dst_file)

    assert command == [IMAGEMAGICK,
                       src_file,
                       dst_file]


def test_default_builder_tiff2jp2(default_builder):
    if sys.platform == "win32":
        src_file = "E:\\mysource\\sample.tif"
        dst_file = "E:\\mysource\\output.jp2"

    else:
        src_file = "/Users/Documents/sample.tif"
        dst_file = "/Users/Documents/output.jp2"

    command = default_builder.build_command(src=src_file, dst=dst_file)

    assert command == [IMAGEMAGICK,
                       src_file,
                       dst_file]


def test_default_builder_tiff2jp2_twoImages(default_builder):
    if sys.platform == "win32":
        src_file = "E:\\mysource\\sample.tif"
        dst_file = "E:\\mysource\\output.jp2"
        src_file2 = "E:\\mysource\\sample2.tif"
        dst_file2 = "E:\\mysource\\output2.jp2"

    else:
        src_file = "/Users/Documents/sample.tif"
        dst_file = "/Users/Documents/output.jp2"
        src_file2 = "/Users/Documents/sample2.tif"
        dst_file2 = "/Users/Documents/output2.jp2"

    command = default_builder.build_command(src=src_file, dst=dst_file)

    assert command == [IMAGEMAGICK,
                       src_file,
                       dst_file]

    command = default_builder.build_command(src=src_file2, dst=dst_file2)
    assert command == [IMAGEMAGICK,
                       src_file2,
                       dst_file2]


def test_ignore_exif_builder_tiff2jp2(monkeypatch):
    """
    Test that the IgnoreExif builder works

    """

    if sys.platform == "win32":
        src_file = "E:\\mysource\\sample.tif"
        dst_file = "E:\\mysource\\output.jpg"
    else:
        src_file = "/Users/Documents/sample.tif"
        dst_file = "/Users/Documents/output.jpg"


    expected_cmd = [IMAGEMAGICK,
                    '-define', 'tiff:exif-properties=false',
                    src_file,
                    dst_file]
    # Because the location of imagemagick is faked for this example,
    # we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command_builder = driver.ImagemagickCommandBuilder(builder=builders.IgnoreExif(),
                                                       program_path=IMAGEMAGICK)

    command = command_builder.build_command(src=src_file, dst=dst_file)
    assert command == expected_cmd
