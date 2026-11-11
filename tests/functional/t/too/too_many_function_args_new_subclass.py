"""Forwarding arguments to a parent ``__new__`` must not emit too-many-function-args."""

# pylint: disable=missing-docstring,unused-argument,too-few-public-methods
import array


class Data(array.array):
    def __new__(cls, data):
        return super().__new__(cls, "b", data)


class Kwargs(array.array):
    def __new__(cls, **kwargs):
        return cls.__new__(cls, **kwargs)


class Own:
    def __new__(cls, first):
        return super().__new__(cls)


Data([1, 2])
Own(1)
Own(1, 2)  # [too-many-function-args]
