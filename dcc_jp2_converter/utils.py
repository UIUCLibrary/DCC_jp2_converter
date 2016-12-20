from pkg_resources import resource_filename, Requirement


def get_config_file():
    return resource_filename(
        Requirement.parse("DCC_jp2_converter"), "settings/settings.ini")
