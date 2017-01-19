from dcc_jp2_converter import file_manager

import pytest
import os


@pytest.fixture
def completed_directory(monkeypatch):
    sample_tree = [
        ('test_tiffs/0852_0019_04', ('access', 'preservation'), ()),
        ('test_tiffs/0852_0019_04/access', (), ('0852_0019_04_001.jp2',
                                                '0852_0019_04_001.tif',
                                                '0852_0019_04_002.jp2',
                                                '0852_0019_04_002.tif',
                                                '0852_0019_04_003.jp2',
                                                '0852_0019_04_003.tif',
                                                '0852_0019_04_004.jp2',
                                                '0852_0019_04_004.tif',
                                                '0852_0019_04_005.jp2',
                                                '0852_0019_04_005.tif',
                                                '0852_0019_04_006.jp2',
                                                '0852_0019_04_006.tif'
                                                '0852_0019_04_007.tif'         # <-- No a matching jp2
                                                )),
        ('test_tiffs/0852_0019_04/preservation/', (), ('0852_0019_04-001.tif',
                                                       '0852_0019_04-002.tif',
                                                       '0852_0019_04-003.tif',
                                                       '0852_0019_04-004.tif',
                                                       '0852_0019_04-005.tif',
                                                       '0852_0019_04-006.tif',
                                                       'Thumbs.db'
                                                       )),
        ('test_tiffs/0852_0020_01', ('access', 'preservation'), ()),
        ('test_tiffs/0852_0020_01/access/', (), ('0852_0020_01_001.jp2',
                                                 '0852_0020_01_001.tif'
                                                 '0852_0020_01_002.jp2'        # <-- No a matching tiff
                                                 )),
        ('test_tiffs/0852_0020_01/preservation/', (), ('0852_0020_01-001.tif',
                                                       '/Thumbs.db'))
    ]

    def get_files(x):
        for x in sample_tree:
            yield x

    monkeypatch.setattr(os, "walk", get_files)
    return sample_tree


def test_pairs_found(completed_directory):
    expected_tiffs = [
        'test_tiffs/0852_0019_04/access/0852_0019_04_001.tif',
        'test_tiffs/0852_0019_04/access/0852_0019_04_002.tif',
        'test_tiffs/0852_0019_04/access/0852_0019_04_003.tif',
        'test_tiffs/0852_0019_04/access/0852_0019_04_004.tif',
        'test_tiffs/0852_0019_04/access/0852_0019_04_005.tif',
        'test_tiffs/0852_0019_04/access/0852_0019_04_006.tif',
        'test_tiffs/0852_0020_01/access/0852_0020_01_001.tif'
    ]

    expected_jp2s = [
        'test_tiffs/0852_0019_04/access/0852_0019_04_001.jp2',
        'test_tiffs/0852_0019_04/access/0852_0019_04_002.jp2',
        'test_tiffs/0852_0019_04/access/0852_0019_04_003.jp2',
        'test_tiffs/0852_0019_04/access/0852_0019_04_004.jp2',
        'test_tiffs/0852_0019_04/access/0852_0019_04_005.jp2',
        'test_tiffs/0852_0019_04/access/0852_0019_04_006.jp2',
        'test_tiffs/0852_0020_01/access/0852_0020_01_001.jp2'
    ]

    for pair in file_manager.find_converted_pair("\ (^_^) /"):
        assert pair.tiff in expected_tiffs
        assert pair.jp2 in expected_jp2s


def test_pairs_match(completed_directory):
    for pair in file_manager.find_converted_pair("\ (^_^) /"):
        assert os.path.splitext(pair.tiff)[0] == os.path.splitext(pair.jp2)[0]
