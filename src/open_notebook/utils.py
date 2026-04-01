"""
Utilities (:mod:`~open_notebook.utils`)
=======================================
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Any


# taken from https://github.com/python-attrs/attrs/blob/main/src/attr/_make.py
class _Missing(enum.Enum):
    """
    Sentinel to indicate the lack of a value when ``None`` is ambiguous.

    If extending attrs, you can use ``typing.Literal[MISSING]`` to show
    that a value may be ``MISSING``.

    .. versionchanged:: 21.1.0 ``bool(MISSING)`` is now False.
    .. versionchanged:: 22.2.0 ``MISSING`` is now an ``enum.Enum`` variant.
    """

    MISSING = enum.auto()

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        return "MISSING"  # pragma: no cover

    def __bool__(self) -> bool:
        return False  # pragma: no cover


MISSING = _Missing.MISSING
"""
Sentinel to indicate the lack of a value when ``None`` is ambiguous.
"""


# taken from https://github.com/conda/conda-lock/blob/main/conda_lock/common.py
def get_in(
    keys: Sequence[Any],
    nested_dict: Mapping[Any, Any],
    default: Any = MISSING,
    factory: Callable[[], Any] | None = None,
) -> Any:
    """
    >>> foo = {"a": {"b": {"c": 1}}}
    >>> get_in(["a", "b"], foo)
    {'c': 1}

    """
    import operator
    from functools import reduce

    try:
        return reduce(  # pyrefly: ignore[no-matching-overload]
            operator.getitem,  # pyrefly: ignore[bad-argument-type]
            keys,
            nested_dict,  # pyrefly: ignore[bad-argument-type]
        )
    except (KeyError, IndexError, TypeError):
        if factory is not None:
            return factory()
        return default
