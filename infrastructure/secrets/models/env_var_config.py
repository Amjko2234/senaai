from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from .env_types import EnvType


@dataclass
class EnvVariable:
    """Configuration for a single environment variable."""

    name: str
    var_type: Type
    required: bool = False
    default: Any = None
    description: str = ""
    validator: Optional[Callable] = None
    env_specific: Optional[Dict[EnvType, Any]] = None

    def __post_init__(self):
        if (self.required) and (self.default is not None):
            # TODO:
            raise ...
