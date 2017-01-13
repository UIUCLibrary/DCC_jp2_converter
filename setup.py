"""DCC_jp2_converter.

Script to create JP2 access images with embedded metadata from tiff access
masters to be used by the Digital Library.

"""
import os
from setuptools import setup
from dcc_jp2_converter import __version__ as version

setup(
    name='DCC_jp2_converter',
    version=version,
    packages=['dcc_jp2_converter',
              'dcc_jp2_converter.exiv2Driver',
              'dcc_jp2_converter.exiv2Driver.exiv2CommandBuilders',
              'dcc_jp2_converter.ImagemagickDriver',
              'dcc_jp2_converter.ImagemagickDriver.imagemagickCommandBuilders',
              'scripts'
              ],
    entry_points={
        'console_scripts': ['makejp2=scripts.cli_convert:main']
    },
    test_suite="tests",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    data_files=[
        ('settings', ['settings/command_paths.ini']),
        (os.path.expanduser("~"), ['settings/command_paths.ini']),
    ],
    zip_safe=False,
    url='https://github.com/UIUCLibrary/DCC_jp2_converter',
    license='',
    author='Henry Borchers',
    author_email='hborcher@illinois.edu',
    description='DCC tool for building JP2 access files from Tiff files'
)
