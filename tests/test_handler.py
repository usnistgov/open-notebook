from __future__ import annotations

import locale
from pathlib import Path

import pytest

from open_notebook.handler import JupyterUrlHandler


@pytest.fixture
def default_handler() -> JupyterUrlHandler:
    return JupyterUrlHandler(
        root="~/top/level",
        host="localhost",
        port="8888",
        dir_prefix="tree",
        file_prefix="notebooks",
    )


def test_handler_relative_path(default_handler: JupyterUrlHandler) -> None:
    h = default_handler

    assert h._path_relative_to_root(Path("~/top/level/a/b")) == Path("a/b")
    assert h._path_relative_to_root(Path("~/top/level/a/b.txt")) == Path("a/b.txt")

    with pytest.raises(ValueError, match=r"Path .*is not a subpath of root.*"):
        h._path_relative_to_root(Path("~/top"))


def test_path_to_url(default_handler: JupyterUrlHandler, tmp_path: Path) -> None:
    h = default_handler
    h.root = tmp_path.absolute()

    other_dir = tmp_path / "a" / "b"
    other_dir.mkdir(parents=True)

    with Path(other_dir / "tmp.ipynb").open(
        "w", encoding=locale.getpreferredencoding(False)
    ) as _:
        pass

    assert h.paths_to_urls(other_dir) == ["http://localhost:8888/tree/a/b"]

    assert h.paths_to_urls(other_dir / "tmp.ipynb") == [
        "http://localhost:8888/notebooks/a/b/tmp.ipynb"
    ]

    assert h.paths_to_urls(other_dir / "tmp.ipynb", suffix="?reset") == [
        "http://localhost:8888/notebooks/a/b/tmp.ipynb?reset"
    ]

    with pytest.raises(ValueError, match=r"Path .*is not a file or directory"):
        h.paths_to_urls(tmp_path / "hello")

    with pytest.raises(ValueError, match=r"Path .*is not a file or directory"):
        h.paths_to_urls(tmp_path / "hello.ipynb")
