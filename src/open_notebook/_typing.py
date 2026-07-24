"""
Typing (:mod:`~open_notebook._typing`)
======================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal  # ruff:ignore[unused-import]

    from ._typing_compat import TypeAlias
    from .utils import _Missing  # ruff:ignore[unused-import]


MISSING_TYPE: TypeAlias = "Literal[_Missing.MISSING]"  # pyrefly: ignore[type-alias-error]
"""Literal MISSING"""
