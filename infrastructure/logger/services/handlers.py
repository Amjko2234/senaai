import logging
from collections.abc import Callable
from pathlib import Path
from typing import List, Optional

from rich.logging import RichHandler

from ....shared.logger.log_levels import LogLevel
from ..filters import Filter
from ..handlers import RichHandlerCfg, RotatingFileHandler

# -----------------------------------------------------------------------------
#   Public functions
# -----------------------------------------------------------------------------


def get_file_handler(
    filename: Path | str,
    fmt: logging.Formatter,
    level: LogLevel | int,
    size_bytes: int,
    backup_count: int,
    encoding: str,
    *,
    filter: Optional[Filter | List[Filter]] = None,
) -> logging.Handler:

    level = level.to_value() if isinstance(level, LogLevel) else level

    handler = RotatingFileHandler(
        filename=filename,
        mode="a",
        maxBytes=size_bytes,
        backupCount=backup_count,
        encoding=encoding,
    )
    handler.setLevel(level)
    handler.setFormatter(fmt)

    if filter is None:
        filters: List[Filter] = []
    elif isinstance(filter, List):
        filters = filter
    else:
        filters = [filter]
    for _filter in filters:
        handler.addFilter(_filter)

    return handler


def get_console_handler(
    fmt: logging.Formatter,
    level: LogLevel | int,
    *,
    filter: Optional[Filter | List[Filter]] = None,
) -> logging.Handler:

    level = level.to_value() if isinstance(level, LogLevel) else level
    handler = RichHandler(
        console=RichHandlerCfg.console.value,
        show_time=RichHandlerCfg.show_time.value,
        show_level=RichHandlerCfg.show_level.value,
        show_path=RichHandlerCfg.show_path.value,
        markup=RichHandlerCfg.markup.value,
        rich_tracebacks=RichHandlerCfg.rich_tracebacks.value,
    )
    handler.setLevel(level)
    handler.setFormatter(fmt)

    if filter is None:
        filters: List[Filter] = []
    elif isinstance(filter, List):
        filters = filter
    else:
        filters = [filter]
    for _filter in filters:
        handler.addFilter(_filter)

    return handler
