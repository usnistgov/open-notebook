from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from open_notebook import config

from .utils import run_inside_dir

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import TypeVar

    T = TypeVar("T")
    YieldFixture = Generator[T]


@pytest.fixture
def home_path() -> Path:
    return Path(__file__).parent.absolute() / "data"


@pytest.fixture
def example_path(tmp_path: Path) -> YieldFixture[Path]:
    other_dir = tmp_path / "a" / "b"
    other_dir.mkdir(parents=True)

    # change to example_path
    old_cwd = Path.cwd()
    os.chdir(tmp_path)

    assert Path.cwd().absolute() == tmp_path.absolute()

    yield tmp_path.absolute()
    # Cleanup?
    os.chdir(old_cwd)


@pytest.fixture
def example_path_with_config(example_path: Path) -> Path:
    config.create_config(
        host="thing",
        port="8889",
        root="~/Documents",
        dir_prefix="tr",
        file_prefix="no",
        overwrite=True,
        path=example_path,
    )

    return example_path


@pytest.fixture
def example_path_with_git(example_path: Path) -> Path:
    run_inside_dir("git init", example_path)

    return example_path


@pytest.fixture
def example_path_with_git_config(
    example_path_with_config: Path, example_path_with_git: Path
) -> Path:
    assert example_path_with_config == example_path_with_git
    return example_path_with_config
