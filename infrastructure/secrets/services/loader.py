from collections.abc import Callable
from pathlib import Path
from typing import Dict, List, Optional

from ....core.exceptions.base import CoreError
from ....shared.utils import PathUtils
from ...logger.services.logger import _ServiceLogger


class _EnvLoader:
    """Handles loading and parsing of .env files."""

    @staticmethod
    def load_env_files(
        file_paths: List[str] | List[Path],
        *,
        logger: Optional[_ServiceLogger] = None,
    ) -> Dict[str, str]:
        """Load environment variables from multiple .env files."""

        env_vars = {}
        for file_path in file_paths:
            if Path(file_path).exists():
                if logger:
                    logger.info(f"Loading environment file: {file_path}")
                # env_vars.update()
            else:
                if logger:
                    logger.debug(f"Environment file not found: {file_path}")
                pass

        return env_vars

    @staticmethod
    def _parse_env_files(file_path: Path | str) -> Dict[str, str]:
        """Parse a .env file."""

        env_vars = {}
        try:
            with PathUtils.open_file(file_path, "r") as file:
                # TODO:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    if "=" not in line:
                        # TODO: log warning
                        continue

                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Handle quoted values
                    if (value.startswith('"') and value.endswith('"')) or (
                        value.startswith("'") and value.endswith("'")
                    ):
                        value = value[1:-1]

                    env_vars[key] = value
        except CoreError as err:
            # TODO: log error
            raise ...
        return env_vars
