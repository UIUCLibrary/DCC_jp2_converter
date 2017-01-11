from pkg_resources import resource_filename, Requirement
from pathlib import Path

def get_config_files():
    config_files = [
        resource_filename(Requirement.parse("DCC_jp2_converter"), "settings/command_paths.ini"),
        str(Path.home() / "command_paths.ini")
    ]
    return config_files
