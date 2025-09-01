import os
from typing import Dict, List, Optional

from ....core.protocols.infrastructure.logger import ServiceLoggerProtocol
from ..models.env_config import EnvConfig
from ..models.loaded_env import LoadedEnv
from .loader import _EnvLoader


class EnvLoaderManager:
    """."""

    def __init__(
        self,
        config: EnvConfig,
        *,
        logger: Optional[ServiceLoggerProtocol] = None,
    ):
        self.config = config
        self.current_env = self._detect_env()

        if logger:
            logger.info(f"Detected environment: {self.current_env.value}")

    def load(
        self,
        override_env: Optional[Dict[str, str]] = None,
    ) -> LoadedEnv:

        file_env = _EnvLoader.load_env_files(self.config.env_file_paths)
        combined_env = {**file_env, **os.environ}

        if override_env:
            combined_env.update(override_env)

        loaded_env: Dict[str, str] = {}
        errors: List[str] = {}

        for env_var in self.config.variables:
            
