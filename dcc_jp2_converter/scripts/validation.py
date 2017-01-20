import os
import sys

from dcc_jp2_converter import exiv2Driver
from dcc_jp2_converter import ImagemagickDriver


def is_executable(path):
    if sys.platform == "win32":
        if os.path.splitext(path)[1].lower() == ".exe":
            return True
        else:
            return False

    # Unix based
    else:
        return os.access(path, os.X_OK)


def find_settings_errors():
    """
    Looks for any configuration errors to make sure that the script can operate properly
    with the given settings by the default path lookup or any changes provided by a
    command_paths.ini file.

    Returns:
        Returns a list of error messages if any. Returns an empty list if found no errors.

    """
    errors = []
    missing_programs = []

    not_found_message = "The following required programs were not found: \"{}\". Please make sure they installed " \
                        "on the path or command_paths.ini file is configured to point to their location in your home " \
                        "folder."

    ########################
    # Imagemagick settings #
    ########################
    imagemagick_path = ImagemagickDriver.get_imagemagick_path()

    # check exists
    if imagemagick_path is None or not os.path.exists(imagemagick_path):
        missing_programs.append("Imagemagick's convert command")
    else:
        # Check if found Windows "convert FAL to NTFS command" by mistake and if the item is executable
        if "system32" in imagemagick_path.lower() or not is_executable(imagemagick_path):
            errors.append("Imagemagick's convert command, \"{}\",is invalid. Check command_paths.ini file.".format(
                imagemagick_path))

    ##################
    # exiv2 settings #
    ##################
    exiv2_path = exiv2Driver.get_exiv2_path()

    # check exists
    if exiv2_path is None or not os.path.exists(exiv2_path):
        missing_programs.append("exiv2")
    else:

        # check is executable
        if not is_executable(exiv2_path):
            errors.append("exiv2 command, \"{}\", is invalid. Check command_paths.ini file.".format(exiv2_path))
    if missing_programs:
        errors.append(not_found_message.format("\", \"".join(missing_programs)))

    return errors


def find_arg_errors(args):
    """
    Perform error check on command line arguments passed in in args to see if
    they are logically valid and return any errors if any are found.
    """

    errors = []

    # You shouldn't be able to use both the remove and the clean option together.
    if args.clean and args.remove:
        errors.append("Invalid argument combination")

    # Make sure that the source directory is valid
    if not os.path.exists(args.path):
        errors.append("Unable to find directory, \"{}\"".format(args.path))

    # Make sure that a path is given, not a file
    if os.path.isfile(args.path):
        errors.append("\"{}\" is not a directory.".format(args.path))

    return errors
