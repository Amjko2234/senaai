import os
from contextlib import contextmanager
from inspect import stack
from pathlib import Path
from typing import IO, Any, Generator

from ....core.exceptions.file import FileNotFoundError
from ....core.exceptions.path import PathNotFoundError


def _validate_file_path(
    path: Path,
    must_exist: bool,
    create_missing_dir: bool,
    file_creation: bool,
    resolve_symlinks: bool,
) -> Path:

    try:
        # Expand ~ (home) and env variables
        # `os.path.expanduser()` e.g., ~ -> /home/
        # `os.path.expandvars()` e.g., $HOME -> /home/
        path = Path(os.path.expandvars(os.path.expanduser(str(path))))

        # Convert relative to absolute
        # Resolve symlinks if necessary, don't worry about missing files
        path = path.resolve(strict=False) if resolve_symlinks else path.absolute()

        # Ensure parent dir exists (or create)
        if not path.parent.exists():
            if create_missing_dir:
                path.parent.mkdir(parents=True, exist_ok=True)
            else:
                raise PathNotFoundError(
                    f"{path.parent} does not exist. Enable `create_missing_dir`"
                )

        # Check file existence rules
        if must_exist and not path.exists():
            raise PathNotFoundError(
                f"{path} does not exist. Enable `create_missing_dir`"
            )
        if not file_creation and not path.exists():
            raise FileNotFoundError(
                f"{path} can not be created. Enable `file_creation`"
            )

        return path
    except OSError as err:
        raise PathNotFoundError(f"System-IO error: {err}")


def _get_file_at_depth(depth: int) -> Path:

    return Path(stack()[depth].filename).resolve()


@contextmanager
def _open_file(
    path: Path | str,
    mode: str,
    encoding: str,
) -> Generator[IO[Any], Any, Any]:
    file = open(path, mode, encoding=encoding)
    try:
        yield file
    finally:
        file.close()
