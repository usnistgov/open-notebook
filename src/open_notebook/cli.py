"""
Program `open-notebook` (:mod:`~open_notebook.cli`)
===================================================
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from open_notebook.utils import MISSING

from .config import DEFAULT_PARAMS

if TYPE_CHECKING:
    from collections.abc import Sequence


# * Logging
FORMAT = "[%(name)s - %(levelname)s] %(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger: logging.Logger = logging.getLogger(__name__)


# * Options


def get_parser() -> argparse.ArgumentParser:
    """Get base parser."""
    parser = argparse.ArgumentParser(
        prog="open-notebook",
        description="Program to open jupyter notebooks from central notebook server.",
        epilog="""
        You can set options with the configuration files ".open-notebook.toml".
        Configuration files are found in the current directory, git root (if in
        a git tracked tree), and the home directory. Note that all these files
        are considered, in order. That is, you could override a single value in
        the current directory, and the rest would be inherited from, in order,
        git root and then the home directory.
        """,
    )

    _ = parser.add_argument(
        "--host",
        type=str,
        default=MISSING,
        help="Host name (default='{host}')".format(**DEFAULT_PARAMS),
    )
    _ = parser.add_argument(
        "-p",
        "--port",
        type=str,
        default=MISSING,
        help="Port (default='{port}')".format(**DEFAULT_PARAMS),
    )
    _ = parser.add_argument(
        "-r",
        "--root",
        default=MISSING,
        help="Directory servers was started in. Defaults to current working directory.",
    )
    _ = parser.add_argument(
        "--dir-prefix",
        type=str,
        default=MISSING,
        help="Directory prefix (default='{dir_prefix}')".format(**DEFAULT_PARAMS),
    )
    _ = parser.add_argument(
        "--file-prefix",
        type=str,
        default=MISSING,
        help="File prefix (default='{file_prefix}')".format(**DEFAULT_PARAMS),
    )
    _ = parser.add_argument("--reset", action="store_true")
    _ = parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=None,
        help="Config style to use.  This is the name of a header in one of the config files.",
    )
    _ = parser.add_argument(
        "--create-config",
        action="store_true",
        help="If passed, create .open-notebook.ini",
    )
    _ = parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Pass to overwrite `~/.open-notebook.toml` if it exists with `--create-config`",
    )
    _ = parser.add_argument(
        "--version", action="store_true", help="Print out program version"
    )
    _ = parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="Set verbosity level.  Can pass multiple times.",
    )
    _ = parser.add_argument("--dry", action="store_true", help="Dry run.")
    _ = parser.add_argument("paths", nargs="*", type=Path, help="file or paths to open")
    return parser


def set_verbosity_level(logger: logging.Logger, verbosity: int | None) -> None:
    """Set verbosity level."""
    if verbosity is None:
        return

    if verbosity < 0:
        level = logging.ERROR
    elif not verbosity:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    logger.setLevel(level)


# * Main program


def get_version_string() -> str:
    """Get version string."""
    from open_notebook import __version__

    return f"open-notebook, {__version__}"


def get_options(
    cli_options: argparse.Namespace,
    section: str | None = None,
    home: str | Path | None = None,
) -> dict[str, Any]:
    """Get option."""
    from open_notebook import config

    options = config.Config.from_config_files(home=home).to_options_dict(
        section=section, **vars(cli_options)
    )
    logger.debug("options: %s", options)
    return options


def create_config(
    options: dict[str, Any],
    paths: list[Path],
    overwrite: bool = False,
    home: str | Path | None = None,
) -> None:
    """Create configuration."""
    from open_notebook import config

    if not (n := len(paths)):
        p = None
    elif n == 1:
        p = paths[0]
    else:
        msg = "can specify zero or one path for config file"
        raise ValueError(msg)

    config.create_config(**options, overwrite=overwrite, path=p, home=home)  # ty: ignore[missing-argument]


def open_paths(options: dict[str, Any], paths: list[Path], dry: bool = False) -> None:
    """Open path as url."""
    from open_notebook import handler

    h = handler.JupyterUrlHandler(**options)  # ty: ignore[missing-argument]

    urls = h.paths_to_urls(paths)

    for url in urls:
        logger.info("opening: %s", url)
        if not dry:
            handler.open_urls(url)  # pragma: no cover


def main(
    args: Sequence[str] | None = None,
    *,
    home: str | Path | None = None,
) -> int:
    """Console script for open_notebook."""
    # get cli options
    parser = get_parser()
    cli_options = (
        parser.parse_args() if args is None else parser.parse_args(args)
    )  # pragma: no cover

    set_verbosity_level(logger=logger, verbosity=cli_options.verbose)
    logger.debug("cli options: %s", cli_options)

    if cli_options.version:
        print(get_version_string())  # noqa: T201

    elif cli_options.create_config:
        create_config(
            options=get_options(cli_options, section=cli_options.config, home=home),
            paths=cli_options.paths,
            overwrite=cli_options.overwrite,
        )

    elif cli_options.paths:
        open_paths(
            options=get_options(cli_options, section=cli_options.config, home=home),
            paths=cli_options.paths,
            dry=cli_options.dry,
        )

    else:
        parser.print_help()
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
