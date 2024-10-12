from model.dataclasses import Profile as DSProfile
from dataclasses import asdict


class Profile(DSProfile):
    def __iter__(self):
        return iter(asdict(self).items())
