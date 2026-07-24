"""
Top level API (:mod:`open_notebook`)
======================================================
"""
# ruff:file-ignore[non-empty-init-module]

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

<<<<<<< before updating
try:
=======
from .core import example_function

try:  # ruff:ignore[non-empty-init-module]
>>>>>>> after updating
    __version__ = _version("open-notebook")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "999"

__author__ = """William P. Krekelberg"""
__email__ = "wpk@nist.gov"


__all__ = [
    "__version__",
]
