from __future__ import annotations

import logging
import os
import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

logger = logging.getLogger(__name__)


@contextmanager
def inside_dir(dirpath: str | Path) -> Generator[None]:
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = Path.cwd()
    try:  # pylint: disable=too-many-try-statements
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def run_inside_dir(
    command: str, dirpath: str | Path | None = None
) -> subprocess.CompletedProcess[bytes]:
    """Run a command from inside a given directory, returning the exit status"""

    if dirpath is None:
        dirpath = Path()

    with inside_dir(dirpath):
        logger.info("Run: %s", command)
        return subprocess.run(shlex.split(command), check=True, stdout=subprocess.PIPE)


def base_options(
    host: str = "localhost",
    port: str = "8888",
    root: str = ".",
    dir_prefix: str = "tree",
    file_prefix: str = "notebooks",
) -> dict[str, Any]:
    return {
        "host": host,
        "port": port,
        "root": Path(root),
        "dir_prefix": dir_prefix,
        "file_prefix": file_prefix,
    }
