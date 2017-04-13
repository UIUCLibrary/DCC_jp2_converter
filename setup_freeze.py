import platform
import os
import dcc_jp2_converter.thirdparty
from cx_Freeze import setup, Executable
from shared_setup import metadata


metadata['options'] = {
    "build_exe": {
        "includes": ["queue", "atexit"],
        "packages": ["os"],
        "excludes": ["tkinter"],
    }
}
metadata['executables'] = [Executable("dcc_jp2_converter/scripts/cli.py",
                                      targetName=("makejp2.exe" if platform.system() == "Windows" else "makejp2"))]

setup(**metadata)
