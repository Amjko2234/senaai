from collections.abc import Callable
from typing import Optional

from ....core.protocols.infrastructure.logger import ServiceLoggerProtocol
from ....infrastructure.config.models.logger_config import LoggerConfig
from ....shared.logger.format_utils import Megabyte
from ....shared.utils import IOUtils
from ..adapters.default_logger import _ServiceLogger
from ..filters import FilterRegistry
from ..formatters import FormatterRegistry
from .handlers import get_console_handler, get_file_handler


class _LoggerFactory:
    """Factory for creating and managing service-specific loggers."""

    # -------------------------------------------------------------------------
    #   Initialization method
    # -------------------------------------------------------------------------

    def create_logger(
        self,
        config: LoggerConfig,
        on_close_callback: Optional[Callable] = None,
    ) -> ServiceLoggerProtocol:
        """Setup handlers based on configuration."""

        _service_name = config.name.lower()

        # Console config
        _console = config.console
        _console_fmt = _console.fmt
        _console_datefmt = _console.datefmt
        _console_level = _console.level.to_value()

        # File config
        _file = config.file
        _file_name = f"{_file.output_name}.log"
        _file_path = _file.output_to / _file_name
        _file_level = _file.level.to_value()
        _file_append = _file.append
        _file_encoding = "utf-8"
        _file_fmt = _file.fmt
        _file_datefmt = _file.datefmt
        _file_max_size_b = Megabyte(int(_file.max_size_mb)).b
        _file_backup_count = _file.backup_count

        console_handler = None
        file_handler = None

        # Not all services should output to console
        # Console handler
        if _console.enabled:
            format = FormatterRegistry.create_fmtter(
                "formatter",
                fmt=_console_fmt,
                datefmt=_console_datefmt,
            )
            filter = FilterRegistry.create_filter("service", service_name=_service_name)
            console_handler = get_console_handler(
                fmt=format,
                level=_console_level,
                filter=filter,
            )

        # File handler
        if _file.enabled:
            if not _file_append:
                IOUtils.clear_content(_file_path)

            format = FormatterRegistry.create_fmtter(
                "context_json",
                fmt=_file_fmt,
                datefmt=_file_datefmt,
            )
            filters = [
                FilterRegistry.create_filter("service", service_name=_service_name),
                FilterRegistry.create_filter("strip_markup"),
            ]
            file_handler = get_file_handler(
                filename=_file_path,
                fmt=format,
                level=_file_level,
                size_bytes=int(_file_max_size_b),
                backup_count=_file_backup_count,
                encoding=_file_encoding,
                filter=filters,
            )

        return _ServiceLogger(
            name=_service_name,
            console_handler=console_handler,
            file_handler=file_handler,
            on_close_callback=on_close_callback,
        )
