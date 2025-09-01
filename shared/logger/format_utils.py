"""Logger configuration formatter utilities."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import NewType, Optional, Tuple, TypeAlias

# ---------------------------------------------------------------
#   New unique data types
# ---------------------------------------------------------------

FileName = NewType("FileName", str)
"""A file name with its extension."""

Bytes: TypeAlias = float
"""Representation of a byte as a float."""

KiloBytes: TypeAlias = float
"""Representation of a kilobyte as a float."""

MegaBytes: TypeAlias = float
"""Representation of a megabyte as a float."""


@dataclass
class Byte:
    """Represents a size in bytes.

    Attributes:
        _b (float): The number of bytes internally

    Properties:
        byte (int): The int equivalent of `_b`.
        kb (float): The equivalent size in KB.
        mb (float): The equivalent size in MB.
    """

    def __init__(self, b: int):
        self._b: Bytes = b

    @property
    def b(self) -> Bytes:
        """Returns the equivalent size in bytes."""
        return self._b

    @property
    def kb(self) -> KiloBytes:
        """Converts the byte value to kilobytes (KB).

        Returns:
            The equivalent size in kilobytes.
        """
        return self._b / 1024

    @property
    def mb(self) -> MegaBytes:
        """Converts the byte value to megabytes (MB).

        Returns:
            The equivalent size in megatbytes.
        """

        return self._b / (1024 * 1024)


@dataclass
class Kilobyte(Byte):
    """Represents a size in kilobytes.

    Internally stored as bytes.

    Attributes:
        byte (int): The size in bytes
                    (1 KB = 1024 bytes).
    """

    def __init__(self, size: int):
        super().__init__(size * 1024)


@dataclass
class Megabyte(Byte):
    """Represents a size in megabytes.

    Internally stored as bytes.

    Attributes:
        byte (int): The size in bytes
                    (1 MB = 1 KB * 1024 bytes).
    """

    def __init__(self, size: int):
        super().__init__(size * 1024 * 1024)


def get_log_path(
    user_path: str | Path, fallback_root: str = "Sena", logname: str | FileName = ""
) -> Tuple[Path, FileName]:
    """Get provided log path, otherwise provide fallback log path.

    Args:
        user_path: Path to log file, either dir path only or
                   included log filename too
        fallback_root: Root dir name as fallback
        logname: Filename for log file

    Returns:
        Either provided log path or fallback log path.
    """
    user_path = Path(user_path)
    logname = FileName(logname)

    try:
        path = user_path / "logs"
        path.parent.mkdir(parents=True, exist_ok=True)
        return (path, logname)
    except Exception:
        # TODO:
        ...

    # Either root's fallback log path or working dir's
    root = _find_parent_dir(fallback_root)
    path = root if root else Path.cwd()

    fallback = path / "logs"
    fallback.parent.mkdir(parents=True, exist_ok=True)
    return (fallback, logname)


def _find_parent_dir(
    root_name: str, start: Path = Path(__file__).resolve()
) -> Optional[Path]:
    """Walks up levels from current dir until root.

    Args:
        root_name: Name of project root dir
        start: Should be the current dir

    Returns:
        Path: Resolved path of project root.
        None: Project root name not found.
    """

    current = start

    # Breaks when reaches os top dir
    while current != current.parent:
        if current.name == root_name:
            return current
        current = current.parent

    return None
