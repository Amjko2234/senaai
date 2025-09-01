import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from ....config.paths import get_relative
from ....core.exceptions.base import CoreError, CoreWarning
from ....core.exceptions.file import FileNotFoundError
from ....core.exceptions.path import PathNotFoundError
from ....core.protocols.infrastructure.logger import ServiceLoggerProtocol
from ....shared.config import ConfigType
from ....shared.utils import PathUtils
from ....shared.utils.str_formatter import blue, bold, green, italic, red, underline
from ..exceptions import UnknownConfigTypeDetector
from ..protocol.type_detector import CfgTypeDetectorProtocol

MIN_YAML_INDICATORS = 0
MIN_YAML_SIGNIFICANCE = 0.3
MIN_REQ_ENV_LINES = 0
MIN_NON_COMMENT_LINES = 0
MIN_ENV_SIGNIFICANCE = 0.7


class _ConfigTypeDetector:

    SUPPORTED_TYPES: Dict[str, ConfigType] = {
        "json": ".json",
        "yaml": ".yaml",
        "env": ".env",
    }

    def __init__(
        self,
        *,
        logger: ServiceLoggerProtocol,
        enable_content_validation: bool = True,
    ):

        self.logger = logger
        self.enable_content_validation = enable_content_validation
        self.detectors: List[Callable[[Path | str], Optional[ConfigType]]] = [
            self._detect_by_extension,
            self._detect_by_content_struct,
            self._detect_by_parsing_attempt,
        ]

    # -------------------------------------------------------------------------
    #   Public methods
    # -------------------------------------------------------------------------

    def detect(
        self,
        file_path: Path | str,
    ) -> ConfigType:

        try:
            path = PathUtils.validate_path(file_path)
        except FileNotFoundError:
            raise
        except PathNotFoundError:
            raise

        detected_type: Optional[ConfigType] = None
        detection_method: Optional[str] = None
        for detector in self.detectors:
            try:
                result = detector(path)
                if result and result in self.SUPPORTED_TYPES:
                    detected_type = result
                    detection_method = detector.__name__
                    self.logger.debug(
                        f"Detected {blue(f'{result.upper()}')} "
                        f"for {underline(f'{get_relative(path)}')} "
                        f"{italic(f'(using {detection_method})')}"
                    )

                    if (self.enable_content_validation) and (
                        not self._validate_detection(path, result)
                    ):
                        self.logger.warning(
                            f"Content validation failed "
                            f"for {underline(f'{get_relative(path)}')} "
                            f"as {blue(f'{result.upper()}')}, trying next detector"
                        )
                        continue

                    break
            except (CoreError, CoreWarning) as err:
                self.logger.debug(
                    f"Detector {underline(f'{detector.__name__}')} failed "
                    f"for {underline(f'{get_relative(path)}')} "
                    f"{red(f'{err}')}"
                )
                continue

        if not detected_type:
            raise UnknownConfigTypeDetector(
                f"Unable to determine config type "
                f"of {underline(f'{get_relative(path)}')} "
                f"supported types are {green(f'{repr(self.SUPPORTED_TYPES)}')}"
            )

        self.logger.info(
            f"Successfully detector {underline(f'{get_relative(path)}')} "
            f"as {blue(f'{detected_type.upper()}')} "
            f"{italic(f'(via {detection_method})')}"
        )
        return detected_type

    # -------------------------------------------------------------------------
    #   Private methods
    #   Main detectors
    # -------------------------------------------------------------------------

    def _detect_by_extension(
        self,
        file_path: Path | str,
    ) -> Optional[str]:
        """Detect type based on file extension."""

        extension = Path(file_path).suffix.lower().replace(".", "")
        return self.SUPPORTED_TYPES.get(extension)

    def _detect_by_content_struct(
        self,
        file_path: Path | str,
    ) -> Optional[str]:
        """Detect type by analyzing content structure patterns."""

        try:
            path = Path(file_path)
            with PathUtils.open_file(path) as file:
                content = file.read().strip()
            if not content:
                return None
            if self._is_json(content):
                return "json"
            if self._is_env(content):
                return "env"
            if self._is_yaml(content):  # More permissive, so last
                return "yaml"
            return None
        except CoreError as err:
            self.logger.debug(
                f"Content struct analysis failed for {get_relative(path)}: {err}"
            )
            return None

    def _detect_by_parsing_attempt(
        self,
        file_path: Path | str,
    ) -> Optional[str]:
        """Detect type by attempting to parse with each format."""

        try:
            path = Path(file_path)
            with PathUtils.open_file(path) as file:
                content = file.read().strip()
            if not content:
                return None
            if self._parse_json(content):  # Stricter parser so prioritize
                return "json"
            if self._parse_yaml(content):  # More permissive, so after json
                return "yaml"
            if self._parse_env(content):
                return "env"
            return None
        except CoreError as err:
            self.logger.debug(
                f"Parse attempt detection failed for {get_relative(path)}: {err}"
            )
            return None

    def _validate_detection(
        self,
        file_path: Path | str,
        detected_type: str,
    ) -> bool:
        """Validate that the detected type can actually parse the file."""

        try:
            path = Path(file_path)
            with PathUtils.open_file(path) as file:
                content = file.read().strip()

            if detected_type == "json":
                return self._parse_json(content)
            elif detected_type == "yaml":
                return self._parse_yaml(content)
            elif detected_type == "env":
                return self._parse_env(content)
            return False

        except CoreError as err:
            self.logger.debug(f"Validation failed for {get_relative(path)}: {err}")
            return False

    # -------------------------------------------------------------------------
    #   Private methods
    #   Helpers for detection by content struct
    # -------------------------------------------------------------------------

    def _is_json(self, content: str) -> bool:
        """Check if content has JSON-like struct."""

        content = content.strip()
        if (content.startswith("{") and content.endswith("}")) or (
            content.startswith("[") and content.endswith("]")
        ):
            return True
        return False

    def _is_yaml(self, content: str) -> bool:
        """Check if content has YAML-like struct."""

        lines = [line for line in content.split("\n") if line.strip()]
        if not lines:
            return False

        yaml_indicators = 0
        total_lines = len(lines)
        for line in lines:
            line = line.strip()
            # Skip comments
            if line.startswith("#"):
                continue
            if ":" in line and not line.startswith("{"):
                # YAML key (patterns)
                if re.match(r"^[a-zA-Z_][a-zA-Z0-9_.-]*\s*:", line):
                    yaml_indicators += 1
                # YAML indentation
                elif line.startswith(" ") and ":" in line:
                    yaml_indicators += 1
            # YAML list (patterns)
            elif line.startswith("- "):
                yaml_indicators += 1
            # YAML document separator
            elif line == "---":
                yaml_indicators += 1

        # Consider significance of portions of matching patterns
        return (
            yaml_indicators > MIN_YAML_INDICATORS
            and (yaml_indicators / total_lines) > MIN_YAML_SIGNIFICANCE
        )

    def _is_env(self, content: str) -> bool:
        """Check if content has ENV file-like struct."""

        lines = [line for line in content.split("\n") if line.strip()]
        if not lines:
            return False

        env_pattern_lines = 0
        for line in lines:
            # Skip comments
            if line.startswith("#"):
                continue
            # Environment key=value pattern
            if "=" in line:
                # Ensure not JSON or YAML
                if not (
                    line.startswith("{")
                    or line.startswith("[")
                    or line.strip().endswith(":")
                    or line.startswith("- ")
                ):
                    # Check for valid ENV variable name
                    key_part = line.split("=")[0].strip()
                    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", key_part):
                        env_pattern_lines += 1

        non_comment_lines = len([line for line in lines if not line.startswith("#")])

        return (
            env_pattern_lines > MIN_REQ_ENV_LINES
            and non_comment_lines > MIN_NON_COMMENT_LINES
            and (env_pattern_lines / non_comment_lines) >= MIN_ENV_SIGNIFICANCE
        )

    # -------------------------------------------------------------------------
    #   Private methods
    #   Helpers for detection by parsing attempt
    # -------------------------------------------------------------------------

    def _parse_json(self, content: str) -> bool:
        """Attempt to parse content as JSON."""

        try:
            json.loads(content)
            return True
        except Exception:
            return False

    def _parse_yaml(self, content: str) -> bool:
        """Attempt to parse content as YAML."""

        try:
            result = yaml.safe_load(content)
            # Additional checks because YAML can parse anything
            return result is not None and not isinstance(result, str)
        except Exception:
            return False

    def _parse_env(self, content: str) -> bool:
        """Attempt to parse content as ENV file."""

        try:
            valid_entries = 0

            lines = [line.strip() for line in content.split("\n") if line.strip()]
            for line in lines:
                # Skip comments
                if line.startswith("#"):
                    continue
                # Key=value line
                if "=" in line:
                    key, _ = line.split("=", 1)
                    # Validate key format
                    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", key.strip()):
                        valid_entries += 1
                    else:
                        return False
                # A non-empty, non-comment line not containing key=value
                elif line:
                    return False
            return valid_entries > 0
        except Exception:
            return False
