from collections.abc import Callable
from pathlib import Path
from typing import Optional, Protocol

from ....shared.config import ConfigType


class CfgTypeDetectorProtocol(Protocol):

    def detect(
        self,
        file_path: Path | str,
    ) -> ConfigType:
        """Detect configuration file type with a multi-stage approach.

        Args:
            file_path (Path | str): Path to configuration file

        Returns:
            Detected file type: 'json', 'yaml', or 'env'

        Raises:
            ...
        """
        ...
