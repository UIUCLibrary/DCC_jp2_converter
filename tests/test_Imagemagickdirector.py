import os
import ImagemagickDriver
import pytest


@pytest.fixture
def default_builder(monkeypatch):
    """Test to make sure that a default command is generated in the case no other preset builder is made"""
    ImagemagickDriver.IMAGEMAGICK = "/usr/bin/convert"

    # Because the location of imagemagick is faked for this example, we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command = ImagemagickDriver.Director(program_path=ImagemagickDriver.IMAGEMAGICK)
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
