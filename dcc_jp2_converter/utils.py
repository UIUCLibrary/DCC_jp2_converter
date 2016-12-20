import pkg_resources


def get_config_file():
    return pkg_resources.resource_filename(pkg_resources.Requirement.parse("DCC_jp2_converter"), "settings/settings.ini")