import platform
import os
import dcc_jp2_converter.thirdparty
from cx_Freeze import setup, Executable
import dcc_jp2_converter
metadata = {
            "packages": ['dcc_jp2_converter',
                         'dcc_jp2_converter.modules',
                         'dcc_jp2_converter.modules.exiv2Driver',
                         'dcc_jp2_converter.modules.exiv2Driver.exiv2CommandBuilders',
                         'dcc_jp2_converter.modules.ImagemagickDriver',
                         'dcc_jp2_converter.modules.ImagemagickDriver.imagemagickCommandBuilders',
                         'dcc_jp2_converter.modules.kakaduDriver',
                         'dcc_jp2_converter.scripts',
                         'dcc_jp2_converter.thirdparty'
                         ],
    "options": {
        "build_exe": {
            "includes": ["queue", "atexit", "six", "pyparsing", "appdirs"],
            "packages": ["os", "packaging"],
            "excludes": ["tkinter"],
            "include_msvcr": True
        }
    }, 'executables': [Executable("dcc_jp2_converter/scripts/cli.py",
                                  targetName=("makejp2.exe" if platform.system() == "Windows" else "makejp2"))]}


setup(
    **metadata,
    name=dcc_jp2_converter.__title__,
    description=dcc_jp2_converter.__description__,
    version=dcc_jp2_converter.__version__,
    author=dcc_jp2_converter.__author__,
    author_email=dcc_jp2_converter.__author_email__,
      )
