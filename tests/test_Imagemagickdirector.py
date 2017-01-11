import os

from dcc_jp2_converter import ImagemagickDriver as driver
from dcc_jp2_converter import imagemagickCommandBuilders as builders

import pytest


@pytest.fixture
def default_builder(monkeypatch):
    """
    Test to make sure that a default command is generated in the case no
    other preset builder is made

    """
    IMAGEMAGICK = "/usr/bin/convert"

    # Because the location of imagemagick is faked for this example,
    # we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command = driver.ImagemagickCommandBuilder(program_path=IMAGEMAGICK)
    return command


def test_default_builder_tiff2jpg(default_builder):
    src_file = "/Users/Documents/sample.tif"
    dst_file = "/Users/Documents/output.jpg"

    command = default_builder.build_command(src=src_file, dst=dst_file)

    assert command == ['/usr/bin/convert',
                       '/Users/Documents/sample.tif',
                       '/Users/Documents/output.jpg']


def test_default_builder_tiff2jp2(default_builder):
    src_file = "/Users/Documents/sample.tif"
    dst_file = "/Users/Documents/output.jp2"

    command = default_builder.build_command(src=src_file, dst=dst_file)

    assert command == ['/usr/bin/convert',
                       '/Users/Documents/sample.tif',
                       '/Users/Documents/output.jp2']


def test_ignore_exif_builder_tiff2jp2(monkeypatch):
    """
    Test that the IgnoreExif builder works

    """
    IMAGEMAGICK = "/usr/bin/convert"
    src_file = "/Users/Documents/sample.tif"
    dst_file = "/Users/Documents/output.jp2"
    expected_cmd = ['/usr/bin/convert',
                    '-define', 'tiff:exif-properties=false',
                    '/Users/Documents/sample.tif',
                    '/Users/Documents/output.jp2']
    # Because the location of imagemagick is faked for this example,
    # we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command_builder = driver.ImagemagickCommandBuilder(builder=builders.IgnoreExif(),
                                                       program_path=IMAGEMAGICK)

    command = command_builder.build_command(src=src_file, dst=dst_file)
    assert command == expected_cmd
