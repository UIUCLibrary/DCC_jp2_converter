import platform
import os
import dcc_jp2_converter.thirdparty
from cx_Freeze import setup, Executable
import dcc_jp2_converter

def create_msi_tablename(python_name, fullname):
    shortname = python_name[:6].replace("_", "").upper()
    longname=fullname
    return "{}|{}".format(shortname, longname)

metadata = {
    "packages": [
        'dcc_jp2_converter',
        'dcc_jp2_converter.modules',
        'dcc_jp2_converter.modules.exiv2Driver',
        'dcc_jp2_converter.modules.exiv2Driver.exiv2CommandBuilders',
        'dcc_jp2_converter.modules.ImagemagickDriver',
        'dcc_jp2_converter.modules.ImagemagickDriver.imagemagickCommandBuilders',
        'dcc_jp2_converter.modules.kakaduDriver',
        'dcc_jp2_converter.scripts',
        'dcc_jp2_converter.thirdparty'
    ],
}
directory_table = [
    (
        "ProgramMenuFolder",        # Directory
        "TARGETDIR",                # Directory_parent
        "PMenu|Programs",           # DefaultDir
    ),
    (
        "PMenu",  # Directory
        "ProgramMenuFolder",  # Directory_parent
        create_msi_tablename(dcc_jp2_converter.__title__, dcc_jp2_converter.FULL_TITLE)
    ),
]
shortcut_table = [
    (
        "startmenuShortcutDoc",      # Shortcut
        "PMenu",                    # Directory_
        "{} Documentation".format(create_msi_tablename(dcc_jp2_converter.__title__, dcc_jp2_converter.FULL_TITLE)),
        "TARGETDIR",                # Component_
        "[TARGETDIR]documentation.url",   # Target
        None,                       # Arguments
        None,                       # Description
        None,                       # Hotkey
        None,                       # Icon
        None,                       # IconIndex
        None,                       # ShowCmd
        'TARGETDIR'                 # WkDir
    ),
]
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
MSVC = os.path.join(PYTHON_INSTALL_DIR, 'vcruntime140.dll')

INCLUDE_FILES = [
    "settings/command_paths.ini",
    "documentation.url",
]
if os.path.exists(MSVC):
    INCLUDE_FILES.append(MSVC)

setup(
    **metadata,
    name=dcc_jp2_converter.FULL_TITLE,
    description=dcc_jp2_converter.__description__,
    version=dcc_jp2_converter.__version__,
    author=dcc_jp2_converter.__author__,
    author_email=dcc_jp2_converter.__author_email__,
    options={
        "build_exe": {
                "includes": ["queue", "atexit", "six", "pyparsing", "appdirs"],
                "packages": ["os"],
                "excludes": ["tkinter"],
                "include_files": INCLUDE_FILES,
                # "include_msvcr": True
            },
        "bdist_msi": {
            "data": {
                "Shortcut": shortcut_table,
                "Directory": directory_table
            }
        }
    },
    executables=[Executable("dcc_jp2_converter/scripts/cli.py",
                            targetName=("makejp2.exe" if platform.system() == "Windows" else "makejp2"))]

)
