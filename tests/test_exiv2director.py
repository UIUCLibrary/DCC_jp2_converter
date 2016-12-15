import os

from dcc_jp2_converter.exiv2Driver import commandBuilders
from dcc_jp2_converter import exiv2Driver


def test_extract_command_builder(monkeypatch):
    DUMMY_EXIV2_PATH = "/usr/bin/exiv2"
    src_file = "/Users/Documents/sample.tif"
    expected_cmd = ['/usr/bin/exiv2', '-eiX', '/Users/Documents/sample.tif']

    # Because the location of exiv2 is faked for this example, we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command_builder = exiv2Driver.Director(builder=commandBuilders.ExtractIPTCCommand(),
                                           program_path=DUMMY_EXIV2_PATH)

    command = command_builder.build_command(src=src_file)

    assert command == expected_cmd


def test_insert_command_builder(monkeypatch):
    DUMMY_EXIV2_PATH = "/usr/bin/exiv2"
    src_file = "/Users/Documents/sample.jp2"
    expected_cmd = ['/usr/bin/exiv2', '-iixX', '/Users/Documents/sample.jp2']

    # Because the location of exiv2 is faked for this example, we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command_builder = exiv2Driver.Director(builder=commandBuilders.InsertIPTCCommand(),
                                           program_path=DUMMY_EXIV2_PATH)
    command = command_builder.build_command(src=src_file)

    assert command == expected_cmd


def test_copyMetadata_command_builder(monkeypatch):

    DUMMY_EXIV2_PATH = "/usr/bin/exiv2"
    src_file = "/Users/Documents/sample.tif"
    dst_file = "/Users/Documents/sample.jp2"
    expected_cmd = ['/usr/bin/exiv2', '-it', '/Users/Documents/sample.tif', '/Users/Documents/sample.jp2']

    # Because the location of exiv2 is faked for this example, we need to ignore the checks
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command_builder = exiv2Driver.Director(builder=commandBuilders.CopyIPTCCommand(),
                                           program_path=DUMMY_EXIV2_PATH)

    command = command_builder.build_command(src=src_file, arg=dst_file)

    assert command == expected_cmd
