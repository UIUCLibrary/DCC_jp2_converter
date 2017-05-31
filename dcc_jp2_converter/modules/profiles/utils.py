from dcc_jp2_converter.modules.profiles import profile, profile_factory


def get_profile(factory_name) -> profile.AbsProfile:
    factory = profile_factory.ProfileFactory()
    new_profile = factory.create_instance(factory_name.lower())
    new_profile.configure()
    return new_profile


def get_all_profiles():
    factory = profile_factory.ProfileFactory()
    return factory.profiles.keys()

