"""Tests for `open-notebook` package."""

from open_notebook import __version__


def test_version() -> None:
<<<<<<< before updating
    assert isinstance(__version__, str)
=======
    from open_notebook import __version__

    assert __version__ != "999"


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
