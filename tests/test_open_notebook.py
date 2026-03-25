"""Tests for `open-notebook` package."""

from open_notebook import __version__


def test_version() -> None:
    assert isinstance(__version__, str)
