from logging import getLogger
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Literal, Optional, overload

from pydantic import BaseModel

from ...core.exceptions.error_codes import ErrorCode
from ..exceptions import RegistryLookupError
from .adapters.logger_builder import LoggerConfigBuilder
from .registry import BUILDER_REGISTRY, BuilderRegistry
from .services.base_builder import BaseConfigBuilder
from .services.factory import _ConfigBuilderFactory


class ConfigBuilderManager:

    # Only init once
    _initialized: Optional[bool] = None
    _instance: Optional["ConfigBuilderManager"] = None
    _lock = Lock()  # Avoid race conditions

    # Created builders at runtime
    _builders: Dict[str, Any] = {}
    # All available registry
    _builder_registry: BuilderRegistry = BUILDER_REGISTRY

    def __new__(cls) -> "ConfigBuilderManager":
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

        self._factory = _ConfigBuilderFactory()
        self._initialized = True

    # -------------------------------------------------------------------------
    #   Public methods
    # -------------------------------------------------------------------------

    def create_builder(
        self,
        builder_type: str,
        path: Path | str,
    ) -> BaseConfigBuilder[BaseModel]:
        """Create or return existing builder instance."""

        if builder_type not in self._builder_registry:
            raise RegistryLookupError(
                message="Failed to look up nonexistent config builder type",
                err_code=ErrorCode.INF_UNK_LOOK_503,
            )

        builder_key = f"{str(path)}/{builder_type}"

        if builder_key not in self._builders:
            with self._lock:
                if builder_key not in self._builders:
                    self._builders[builder_key] = self._factory.create_builder(
                        builder_type,
                        Path(path),
                    )

        return self._builders[builder_key]


# -----------------------------------------------------------------------------
#   Public API
# -----------------------------------------------------------------------------

# Global factory instance
config_builder_manager = ConfigBuilderManager()


@overload
def create_config_builder(
    builder_type: Literal["logger"],
    path: Path | str,
) -> LoggerConfigBuilder: ...


@overload
def create_config_builder(
    builder_type: str,
    path: Path | str,
) -> BaseConfigBuilder[BaseModel]: ...


def create_config_builder(
    builder_type: str,
    path: Path | str,
) -> BaseConfigBuilder[BaseModel]:
    """Create or return existing builder instance.

    Args:
        builder_type: Name of the config builder instance
        path: Path to the JSON config file

    Raises:
        TypeError: A missing or unwanted

    Returns:
        Config builder.
    """

    return config_builder_manager.create_builder(builder_type, path)
