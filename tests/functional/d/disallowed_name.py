# pylint: disable=missing-docstring,too-few-public-methods,attribute-defined-outside-init,unused-argument

from typing import Final

def baz():  # [disallowed-name]
    pass

class foo():  # [disallowed-name]
    pass

foo = {}.keys()  # [disallowed-name]
foo = 42  # [disallowed-name]
aaa = 42  # [invalid-name]


class Base:
    def toto(self):  # [disallowed-name]
        pass

    def fine(self, arg):
        self.tutu = 1  # [disallowed-name]


class Child(Base):
    def toto(self):  # [disallowed-name]
        pass

    def fine(self, arg):
        self.tutu = 2  # [disallowed-name]
        self.other = 4

    def good_name(self):
        pass


class FinalHolder:
    def __init__(self):
        self.tata: Final = 1  # [disallowed-name]
        self.ok: Final = 2
