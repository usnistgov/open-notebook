from __future__ import annotations

import os
import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import logging

logger = logging.getLogger(__name__)


@contextmanager
def inside_dir(dirpath: str | Path) -> Iterator[None]:
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = Path.cwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def run_inside_dir(
    command: str, dirpath: str | Path | None = None
) -> subprocess.CompletedProcess[bytes]:
    """Run a command from inside a given directory, returning the exit status"""

    if dirpath is None:
        dirpath = Path(".")

    with inside_dir(dirpath):
        logger.info(f"Run: {command}")
        return subprocess.run(shlex.split(command), check=True, stdout=subprocess.PIPE)
