import sys

import os
from dcc_jp2_converter import KakaduCommandBuilder
from dcc_jp2_converter import kakaduCommandBuilders as builders
import dcc_jp2_converter

if sys.platform == "win32":
    KAKADU_COMPRESS = "C:\\Program Files\\kakadu\\kdu_compress.exe"
else:
    KAKADU_COMPRESS = "/usr/bin/kdu_compress"


def mockreturn():
    return KAKADU_COMPRESS


def test_simple(monkeypatch):
    if sys.platform == "win32":
        src_file1 = "E:\\mysource\\sample.tif"
        src_file2 = "E:\\mysource\\sample2.tif"
        dst_file1 = "E:\\mysource\\output.jp2"
        dst_file2 = "E:\\mysource\\output2.jp2"

    else:
        src_file1 = "/Users/Documents/sample.tif"
        src_file2 = "/Users/Documents/sample2.tif"
        dst_file1 = "/Users/Documents/output.jp2"
        dst_file2 = "/Users/Documents/output2.jp2"

    monkeypatch.setattr(os.path, "exists", lambda x: True)
    monkeypatch.setattr(dcc_jp2_converter.kakaduDriver, "get_kdu_compress_path", lambda: KAKADU_COMPRESS)
    command_builder = KakaduCommandBuilder(builder=builders.Simple(), program_path=KAKADU_COMPRESS)
    command = command_builder.build_command(src=src_file1, dst=dst_file1)

    assert command == [KAKADU_COMPRESS, "-quiet", "-i", src_file1, "-o", dst_file1]

    command = command_builder.build_command(src=src_file2, dst=dst_file2)
    assert command == [KAKADU_COMPRESS, "-quiet", "-i", src_file2, "-o", dst_file2]


def test_HathiPreset(monkeypatch):
    if sys.platform == "win32":
        src_file1 = "E:\\mysource\\sample.tif"
        src_file2 = "E:\\mysource\\sample2.tif"
        dst_file1 = "E:\\mysource\\output.jp2"
        dst_file2 = "E:\\mysource\\output2.jp2"

    else:
        src_file1 = "/Users/Documents/sample.tif"
        src_file2 = "/Users/Documents/sample2.tif"
        dst_file1 = "/Users/Documents/output.jp2"
        dst_file2 = "/Users/Documents/output2.jp2"

    monkeypatch.setattr(dcc_jp2_converter.kakaduDriver, "get_kdu_compress_path", lambda: KAKADU_COMPRESS)
    monkeypatch.setattr(os.path, "exists", lambda x: True)

    command_builder = KakaduCommandBuilder(builder=builders.HathiPreset(), program_path=KAKADU_COMPRESS)
    command = command_builder.build_command(src=src_file1, dst=dst_file1)

    assert command == [KAKADU_COMPRESS, "-quiet", "-i", src_file1, "-o", dst_file1, "Clevels=5", "Clayers=8", "Corder=RLCP",
                       "Cuse_sop=yes", "Cuse_eph=yes", "Cmodes=RESET|RESTART|CAUSAL|ERTERM|SEGMARK", "-no_weights",
                       "-slope", "42988", "-jp2_space", "sRGB"]

    command = command_builder.build_command(src=src_file2, dst=dst_file2)
    assert command == [KAKADU_COMPRESS, "-quiet", "-i", src_file2, "-o", dst_file2, "Clevels=5", "Clayers=8", "Corder=RLCP",
                       "Cuse_sop=yes", "Cuse_eph=yes", "Cmodes=RESET|RESTART|CAUSAL|ERTERM|SEGMARK", "-no_weights",
                       "-slope", "42988", "-jp2_space", "sRGB"]
