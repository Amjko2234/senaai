from dataclasses import dataclass
from typing import List

from pydantic import Field

from .env_var_config import EnvVariable


@dataclass
class EnvConfig:
    """Configuration container for all environment variables."""

    variables: List[EnvVariable]
    env_file_paths: List[str] = Field(default_factory=lambda: [".env", ".env.local"])
    env_prefix: str = ""
    case_sensitive: bool = True

    def __post_init__(self):
        # Validate no duplicate variable names
        names = [var.name for var in self.variables]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            # TODO:
            raise ...
