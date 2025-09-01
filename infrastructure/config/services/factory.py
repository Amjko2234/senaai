"""Factory module for constructing config builder instances.

This module centralizes logic for retrieving and instantiating builder classes
from a global registry (`BUILDER_REGISTRY`). Intended to be the single entry
point for config builder creation.
"""

from pathlib import Path
from typing import Any, List, Literal, Optional, overload

import jsonschema
from pydantic import BaseModel

from ....shared.config import ConfigValues, EnvConfig, JsonConfig, YamlConfig
from ....shared.utils import IOUtils
from ...logger import LoggerManager
from ..adapters.type_detector import _ConfigTypeDetector
from ..protocol.type_detector import CfgTypeDetectorProtocol
from ..registry import BUILDER_REGISTRY, VALIDATION_REGISTRY, ValidationEntry
from .base_builder import BaseConfigBuilder


class _ConfigBuilderFactory:
    """Factory for producing config builder instances.

    This class should not be instantiated; use it as a static interface.
    """

    # All available registry
    _builder_registry = BUILDER_REGISTRY
    _validation_registry = VALIDATION_REGISTRY

    # Type of config detector
    _cfg_type_detector: Optional[CfgTypeDetectorProtocol] = _ConfigTypeDetector(
        logger=LoggerManager().system_logger
    )

    # -------------------------------------------------------------------------
    #   Public method
    # -------------------------------------------------------------------------

    def create_builder(
        self,
        builder_type: str,
        path: Path,
        format: Optional[Literal["json", "yaml", "env"]] = None,
    ) -> BaseConfigBuilder[BaseModel]:

        if not path.exists():
            # TODO:
            raise ...

        if builder_type not in self._builder_registry:
            # TODO:
            raise ...
        if builder_type not in self._validation_registry:
            # TODO:
            raise ...

        # Create builder after validation
        config_data = self._get_config(path, format)
        validated_config = self._validate_data(builder_type, config_data)
        builder_reg = self._builder_registry[builder_type]["builder_class"]
        return builder_reg(validated_config)

    @classmethod
    def get_builders(cls) -> List[str]:
        """Get the list of available builder types."""

        return list(cls._builder_registry.keys())

    @classmethod
    def get_validation_info(cls, builder_type: str) -> ValidationEntry:
        """Get the validation config for a builder type."""

        if builder_type not in cls._validation_registry:
            # TODO:
            raise ...
        return cls._validation_registry[builder_type]

    # -------------------------------------------------------------------------
    #   Utility/helper methods
    # -------------------------------------------------------------------------

    # def _get_section(
    #     self,
    #     path: Path,
    #     section: str,
    # ) -> ConfigValues:
    #     """Get specific section from a config file."""
    #
    #     config_data = IOUtils.load_json(path)
    #     return config_data.get(section, {})

    @overload
    def _get_config(
        self,
        path: Path,
        format: Literal["env"],
    ) -> EnvConfig: ...

    @overload
    def _get_config(
        self,
        path: Path,
        format: Literal["yaml"],
    ) -> YamlConfig: ...

    @overload
    def _get_config(
        self,
        path: Path,
        format: Literal["json"],
    ) -> JsonConfig: ...

    @overload
    def _get_config(
        self,
        path: Path,
        format: None = None,
    ) -> ConfigValues: ...

    def _get_config(
        self,
        path: Path,
        format: Optional[Literal["json", "yaml", "env"]] = None,
    ) -> ConfigValues:
        """Load config data from file with format-specific typing."""

        config_type = format or self._cfg_type_detector.detect(path)
        match config_type:
            case "json":
                return IOUtils.load_json(path)
            case "yaml":
                return IOUtils.load_yaml(path)
            case "env":
                return IOUtils.load_env(path)
            case _:
                # TODO:
                raise ...

    def _validate_data(
        self,
        builder_type: str,
        config_data: Any,
    ) -> Any:
        """Apply validation based on registry config."""

        builder_entry = self._builder_registry[builder_type]
        validation_entry = self._validation_registry[builder_type]

        # Check expected data type
        if not isinstance(config_data, validation_entry["expected_type"]):
            # TODO:
            raise ...

        strategy = validation_entry["strategy"]
        if strategy == "pydantic":
            return builder_entry["config_class"](**config_data)
        elif strategy == "jsonschema":
            schema = validation_entry["schema"]
            if schema is None:
                # TODO:
                raise ...
            jsonschema.validate(config_data, schema)
            return config_data
        elif strategy is None:
            return config_data
        else:
            # TODO:
            raise ...
