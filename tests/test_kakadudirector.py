import sys
import pytest
import os
# from dcc_jp2_converter import kakaduDriver as driver
from dcc_jp2_converter import KakaduCommandBuilder
from dcc_jp2_converter import kakaduCommandBuilders as builders

if sys.platform == "win32":
    KAKADU_COMPRESS = "C:\\Program Files\\kakadu\\kdu_compress.exe"
else:
    KAKADU_COMPRESS = "/usr/local/bin/kdu_compress"


# @pytest.fixture
# def default_builder(monkeypatch):
#     """
#     Test to make sure that a default command is generated in the case no
#     other preset builder is made
#
#     """
#
#     # Because the location of kakadu compress is faked for this example,
#     # we need to ignore the checks
#     monkeypatch.setattr(os.path, "exists", lambda x: True)
#     command_builder = KakaduCommandBuilder(builder=builders.Simple(), program_path=KAKADU_COMPRESS)
#     command = command_builder.build_command
#     # command = driver.KakaduCommandBuilder(builder=builders.simple()m program_path=KAKADU_COMPRESS)
#     return command


def test_simple(monkeypatch):
    if sys.platform == "win32":
        src_file = "E:\\mysource\\sample.tif"
        dst_file = "E:\\mysource\\output.jp2"

    else:
        src_file = "/Users/Documents/sample.tif"
        dst_file = "/Users/Documents/output.jp2"

    monkeypatch.setattr(os.path, "exists", lambda x: True)
    command_builder = KakaduCommandBuilder(builder=builders.Simple(), program_path=KAKADU_COMPRESS)
    command = command_builder.build_command(src=src_file, dst=dst_file)

    assert command == [KAKADU_COMPRESS, "-i", src_file, "-o", dst_file]


def test_HathiPreset(monkeypatch):
    if sys.platform == "win32":
        src_file = "E:\\mysource\\sample.tif"
        dst_file = "E:\\mysource\\output.jp2"

    else:
        src_file = "/Users/Documents/sample.tif"
        dst_file = "/Users/Documents/output.jp2"

    monkeypatch.setattr(os.path, "exists", lambda x: True)
    command_builder = KakaduCommandBuilder(builder=builders.HathiPreset(), program_path=KAKADU_COMPRESS)
    command = command_builder.build_command(src=src_file, dst=dst_file)

    assert command == [KAKADU_COMPRESS, "-i", src_file, "-o", dst_file, "Clevels=5", "Clayers=8", "Corder=RLCP",
                       "Cuse_sop=yes", "Cuse_eph=yes", "'Cmodes=RESET|RESTART|CAUSAL|ERTERM|SEGMARK'", "-no_weights",
                       "-slope", "42988"]
