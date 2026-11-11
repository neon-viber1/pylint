"""Subscripting a value with several inferred results (issue 10423)."""
# pylint: disable=missing-function-docstring,too-few-public-methods,invalid-name,expression-not-assigned
from unknown_module import subplots  # pylint: disable=import-error


def uninferable_second(figsize, ncols):
    if not isinstance(figsize[0], int):
        return figsize
    return subplots(figsize=(ncols * figsize[0], figsize[1]), ncols=ncols)


def only_unsupported(flag):
    if flag:
        return 1
    return 2


def int_or_list(flag):
    if flag:
        return 1
    return [1, 2]


def int_or_uninferable(flag):
    if flag:
        return 1
    return subplots()


# Several results, one of them uninferable or subscriptable: no message.
single = uninferable_second((4, 7), 3)
single[0].plot()
single.tight_layout()
int_or_list(True)[0]
int_or_uninferable(True)[0]

# Every result is concrete and unsupported: still reported.
only_unsupported(True)[0]  # [unsubscriptable-object]

# Known limitation: tuple unpacking of a call result loses the uninferable
# alternative inside astroid, so only the first return type is considered.
fig, axes = uninferable_second((4, 7), 3)
axes[0].plot()  # [unsubscriptable-object]
fig.tight_layout()  # [no-member]
