from typing import List

from .models.env_config import EnvConfig
from .models.env_var_config import EnvVariable
from .models.loaded_env import LoadedEnv
from .services.manager import EnvLoaderManager


def create_basic_config(variables: List[EnvVariable]) -> EnvConfig:
    """Create a basic configuration with common defaults."""

    return EnvConfig(variables=variables)


def load_environment(config: EnvConfig) -> LoadedEnv:
    """Convenience function to load environment with configuration."""

    return EnvLoaderManager(config).load()
