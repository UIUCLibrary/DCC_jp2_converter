from __future__ import print_function
import pkg_resources
import os

import sys

def get_config_files():
    config_files = []

    # Get the default settings first
    try:
        config_files.append(pkg_resources.resource_filename(pkg_resources.Requirement.parse("DCC_jp2_converter"),
                                                            "settings/command_paths.ini"), )
    except pkg_resources.DistributionNotFound:
        print("Default command_paths.ini settings file not found", file=sys.stderr)
        pass

    # Get Any alternative settings
    config_files.append(os.path.join(os.path.expanduser("~"), "command_paths.ini"))
    if config_files:
        return config_files
    raise FileNotFoundError("No config files found")
