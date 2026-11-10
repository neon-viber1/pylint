"""Regression test for issue 11119: classmethod constructor called on a subclass."""
# pylint: disable=too-few-public-methods,missing-docstring


class A:
    @classmethod
    def create(cls):
        return cls()


class B(A):
    def new_method(self):
        return 1


# ``cls()`` must be inferred as the class the method was called on (B), not A.
B.create().new_method()
B().new_method()
