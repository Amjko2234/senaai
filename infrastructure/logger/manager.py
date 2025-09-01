import sys
from contextlib import contextmanager
from threading import Lock
from typing import Dict, Optional, Set

from ...config.logger.static import SYSTEM_LOGGER_CONFIG
from ...core.exceptions.error_codes import ErrorCode
from ...core.protocols.infrastructure.logger import ServiceLoggerProtocol
from ...infrastructure.config.models import LoggerConfig
from ..exceptions import LookupError
from .services.factory import _LoggerFactory


class LoggerManager:
    """Manager to orchestrate setup and creating loggers."""

    # Only init once
    _initialized: Optional[bool] = None
    _instance: Optional["LoggerManager"] = None
    _lock = Lock()  # Avoid race conditions

    # Track active loggers
    active_loggers: Dict[str, ServiceLoggerProtocol] = {}
    _system_logger: Optional[ServiceLoggerProtocol] = None
    global_exception_handler_set: bool = False

    def __new__(cls) -> "LoggerManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):

        # Already initialized
        if getattr(self, "_initialized", False):
            return

        self.factory = _LoggerFactory()
        if not self.global_exception_handler_set:
            self._setup_global_exception_handler()
        self._create_system_logger()
        self._initialized = True

    # -------------------------------------------------------------------------
    #   Properties
    # -------------------------------------------------------------------------

    @property
    def system_logger(cls) -> ServiceLoggerProtocol:
        """Get global system logger.

        Is automatically created when it's not.
        """

        if cls._system_logger is None:
            logger = cls._create_system_logger()
        return cls._system_logger or logger

    # -------------------------------------------------------------------------
    #   Methods for service use
    # -------------------------------------------------------------------------

    def create_logger(self, config: LoggerConfig) -> ServiceLoggerProtocol:
        """Create a new logger instance for a service"""

        with self._lock:
            if config.name in self.active_loggers:
                # Don't log because its not yet initialized
                raise LookupError(
                    message=f"{config.name} logger cannot be created, for it already exists",
                    err_code=ErrorCode.INF_LOGR_LOOK_526,
                )

            logger = self.factory.create_logger(
                config=config,
                on_close_callback=self._on_logger_closed,
            )

            self.active_loggers[f"{config.name}"] = logger
            logger.info(f"{config.name} logger initialized")

            return logger

    @classmethod
    def get_logger(cls, service_name: str) -> ServiceLoggerProtocol:
        """Get an existing logger by service name."""

        logger = cls.active_loggers[service_name]

        # Was already closed using logger's `.close` method
        if logger and logger.closed:
            del logger

        return logger

    @classmethod
    def list_active_loggers(cls) -> Set[str]:
        """Get service names of all active loggers."""

        return set(cls.active_loggers.keys())

    # -------------------------------------------------------------------------
    #   Private helper methods
    #   For system uncaught exceptions
    # -------------------------------------------------------------------------

    def _create_system_logger(self) -> ServiceLoggerProtocol:
        """Create a dedicated system logger for uncaught exceptions."""

        system_config = LoggerConfig(**SYSTEM_LOGGER_CONFIG)
        system_logger = self.factory.create_logger(system_config)
        self._system_logger = system_logger
        self.system_logger.debug("System logger initialized")
        self.active_loggers[system_config.name] = system_logger

        return system_logger

    def _setup_global_exception_handler(self):
        """Setup system-wide exception handler."""

        # Preserve original hook because `sys.excepthook` will be
        # overriden later with custom except hook
        original_excepthook = sys.excepthook

        # Custom except hook
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                original_excepthook(exc_type, exc_value, exc_traceback)
                return

            system_logger = self.system_logger
            system_logger.critical(
                "Uncaught system exception",
                exc_type=exc_type.__name__,
                exc_value=str(exc_value),
                exc_info=(exc_type, exc_value, exc_traceback),
            )

        sys.excepthook = handle_exception

    # -------------------------------------------------------------------------
    #   Temporary logger method
    #   Use when entering runtime context
    # -------------------------------------------------------------------------

    @contextmanager
    def temporary_logger(self, config: LoggerConfig):
        """Context manager for temporary logger that auto-closes."""

        logger = self.create_logger(config)
        try:
            yield logger
        finally:
            logger.close()

    # -------------------------------------------------------------------------
    #   Close logger method
    # -------------------------------------------------------------------------

    def _on_logger_closed(self, service_name: str):
        """Called when a `_ServiceLogger` closes itself."""

        with self._lock:
            if service_name in self.active_loggers:
                del self.active_loggers[service_name]

    def close_all(self):
        """Close all active loggers."""

        with self._lock:
            for logger in list(self.active_loggers.values()):
                logger.close()
                del logger
            self.active_loggers.clear()


# Global factory instance
logger_manager = LoggerManager()


# -----------------------------------------------------------------------------
#   Public API
# -----------------------------------------------------------------------------


def create_logger(config: LoggerConfig) -> ServiceLoggerProtocol:
    """Utility function to create a service-specific logger.

    Args:
        name (str | FileName): Name of the service-specific logger
        path (str | Path): Path for the log file
        kwargs (Dict[str, ...]): Other configurations

    Returns:
        _ServiceLogger: A logger whose name is the service name.
    """

    return logger_manager.create_logger(config)
