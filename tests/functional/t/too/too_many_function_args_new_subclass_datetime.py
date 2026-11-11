"""Subclassing datetime.datetime and forwarding to ``super().__new__``."""

# pylint: disable=missing-docstring,unused-argument,too-many-positional-arguments,too-many-arguments
import datetime
from typing import Self


class MyDateTime(datetime.datetime):
    def __new__(
        cls,
        firstArg: object,
        month: int | None = None,
        day: int | None = None,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> Self:
        return super().__new__(
            cls, firstArg, month, day, hour, minute, second, microsecond
        )


MyDateTime(1, 1, 1)
