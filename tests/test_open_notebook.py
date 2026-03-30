"""Tests for `open-notebook` package."""

<<<<<<< before updating
from open_notebook import __version__


def test_version() -> None:
    assert isinstance(__version__, str)
=======
from __future__ import annotations

import re

import pytest

from open_notebook import example_function


def test_version() -> None:
    from open_notebook import __version__

    assert isinstance(__version__, str)
    assert re.match(r"^\d+\.\d+\.\d+.*$", __version__) is not None


@pytest.fixture
def response() -> tuple[int, int]:
    return 1, 2


def test_example_function(response: tuple[int, int]) -> None:
    expected = 3
    assert example_function(*response) == expected


def test_command_line_interface() -> None:
    from open_notebook import cli

    assert not cli.main([])
>>>>>>> after updating
