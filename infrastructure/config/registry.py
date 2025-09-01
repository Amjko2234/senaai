from typing import Any, Dict, Literal, Optional, Type, TypeAlias, TypedDict

from pydantic import BaseModel

from .adapters import LoggerConfigBuilder
from .models import LoggerConfig
from .services import BaseConfigBuilder


class BuilderEntry(TypedDict):
    "How a value in a builder registry should be."

    builder_class: Type[BaseConfigBuilder]
    config_class: Type[BaseModel]


class ValidationEntry(TypedDict):
    "How a value in a validation registry should be."

    strategy: Optional[Literal["pydantic", "jsonschema"]]
    schema: Optional[Dict[str, Any]]
    expected_type: Type


BuilderRegistry: TypeAlias = Dict[str, BuilderEntry]
ValidationRegistry: TypeAlias = Dict[str, ValidationEntry]

# -----------------------------------------------------------------------------
#   Registry constants
# -----------------------------------------------------------------------------

BUILDER_REGISTRY: BuilderRegistry = {
    "logger": {
        "builder_class": LoggerConfigBuilder,
        "config_class": LoggerConfig,
    },
}

VALIDATION_REGISTRY: ValidationRegistry = {
    "logger": {
        "strategy": "pydantic",
        "schema": None,
        "expected_type": dict,
    },
}
