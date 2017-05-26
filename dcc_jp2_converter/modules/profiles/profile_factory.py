from inspect import getmembers, isclass, isabstract
from dcc_jp2_converter.modules import profiles


class ProfileFactory:
    profiles = {}

    def __init__(self):
        self.load_packages()

    def load_packages(self):

        classes = getmembers(profiles, lambda m: isclass(m) and not isabstract(m))
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, profiles.profile.AbsProfile):
                self.profiles.update([[name, _type]])

    def create_instance(self, profile_name):
        return self.profiles[profile_name]()
