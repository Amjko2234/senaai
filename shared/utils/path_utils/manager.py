from contextlib import contextmanager
from pathlib import Path
from typing import IO, Any, BinaryIO, Generator, Literal, TextIO, overload

# from .services.file_validator import validate_file_path
# from .services.root_finder import find_project_root
from ._services import _get_file_at_depth, _open_file, _validate_file_path


class PathUtils:

    @classmethod
    def get_file_depth(
        cls,
        depth: int = 1,
    ) -> Path:
        """Get the file path at a given stack depth.

        Args:
            depth (int): The desired stack depth

        depth=1  -> immediate caller
        depth=2  -> caller's caller
        depth=-1 -> top-level entry script

        Returns:
            The absolute path at stack depth.
        """

        return _get_file_at_depth(depth)

    @overload
    @classmethod
    @contextmanager
    def open_file(
        cls,
        path: Path | str,
        mode: Literal["r"] = "r",
        *,
        encoding: str = "utf-8",
    ) -> Generator[TextIO, Any, Any]: ...

    @overload
    @classmethod
    @contextmanager
    def open_file(
        cls,
        path: Path | str,
        mode: Literal["rb"],
        *,
        encoding: str = "utf-8",
    ) -> Generator[BinaryIO, Any, Any]: ...

    @overload
    @classmethod
    @contextmanager
    def open_file(
        cls,
        path: Path | str,
        mode: str,
        *,
        encoding: str,
    ) -> Generator[IO[Any], Any, Any]: ...

    @classmethod
    @contextmanager
    def open_file(
        cls,
        path: Path | str,
        mode: Literal["r", "rb"] = "r",
        *,
        encoding: Literal["utf-8"] = "utf-8",
    ) -> Generator[IO[Any], Any, Any]:
        """Opens a file.

        Args:
            path (Path | str): Path string or object (absolute or relative)
            mode (str): Mode to read file, only either `r` or `rb`
            encoding: Encoding system for reading file's contents, only `utf-8`

        Note:
            Use with `with` statement.

        Returns:
            Yielded the opened file.
        """

        with _open_file(path, mode, encoding) as file:
            yield file

    @classmethod
    def validate_path(
        cls,
        path: Path | str,
        *,
        must_exist: bool = False,
        create_missing_dir: bool = False,
        file_creation: bool = True,
        resolve_symlinks: bool = True,
    ) -> Path:
        """Validates and normalizes a file path.

        Args:
            path (Path | str): Path string or object (absolute or relative)
            must_exist (bool): If True, raises an error if the file does not exist
            create_missing_dir (bool): If True, creates parent directory if missing
            file_creation (bool): If False, raises an error if the file does not
                exist yet
            resolve_symlinks (bool): If True, resolves symbolic links to the real
                path

        Returns:
            Validated absolute Path object

        Raises:
            PathNotFoundError: Failed to access/create path from specified path.
            FileNotFoundError: Failed to access/craete file from specified path.
        """

        return _validate_file_path(
            Path(path),
            must_exist,
            create_missing_dir,
            file_creation,
            resolve_symlinks,
        )
