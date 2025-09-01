from pathlib import Path
from typing import Any, Dict, Optional, Type

from ...config import ConfigValues
from ._services import _clear_content, _load_env, _load_json, _load_yaml, _write


class IOUtils:

    @classmethod
    def load_env(
        cls,
        path: Path,
        expect: Optional[Type[dict]] = dict,
    ) -> Dict[str, str | None]:
        """Load all ENV values from disk.

        Args:
            path (Path): Path to the ENV file

        Returns:
            Parsed ENV content.
        """

        return _load_env(path, expect=expect)

    @classmethod
    def load_json(
        cls,
        path: Path | str,
        *,
        encoding: str = "utf-8",
        schema: Optional[Path] = None,
        expect: Optional[Type[Any]] = None,
    ) -> ConfigValues:
        """Load a JSON file from disk.

        Args:
            path (Path): Path to the JSON file
            encoding (str): Type of text encoding system
                Defaults to 'utf-8'
            schema (Path): Path to the jsonschema file for validation
                Defaults to None
            expect (Type): Expected data type to return
                Defaults to None

        Returns:
            Parsed JSON content.
        """

        return _load_json(
            Path(path),
            encoding=encoding,
            schema=schema,
            expect=expect,
        )

    @classmethod
    def load_yaml(
        cls,
        path: Path,
        *,
        encoding: str = "utf-8",
        expect: Optional[Type[Any]] = None,
    ) -> ConfigValues:
        """Load a YAML file from disk.

        Args:
            path (Path): Path to the YAML file
            encoding (str): Type of text encoding system
                Defaults to 'utf-8'

        Returns:
            Parsed YAML content.
        """

        return _load_yaml(path, encoding=encoding, expect=expect)

    @classmethod
    def write(
        cls,
        content: str,
        path: Path,
        *,
        encoding: str = "utf-8",
    ) -> None:
        """Write into a file.

        Args:
            path (Path): Path to the file
            encoding (str): Type of text encoding system
                Defaults to 'utf-8'
        """

        return _write(content, path, encoding=encoding)

    @classmethod
    def clear_content(
        cls,
        path: Path,
        *,
        encoding: str = "utf-8",
    ) -> None:
        """Clear contents of a file.

        Args:
            path (Path): Path to the file
            encoding (str): Type of text encoding system
                Defaults to 'utf-8'

        Note:
            Uses `write` as backend.
        """

        return _clear_content(path, encoding=encoding)
