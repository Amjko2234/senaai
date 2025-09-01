from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ....core.exceptions.error_codes import ErrorCode
from ....shared.logger import LogLevel, Megabyte, MegaBytes
from ..exceptions import MissingConfigValueError
from .base_config import BaseConfig

# -----------------------------------------------------------------------------
#   Parent base model
# -----------------------------------------------------------------------------


class ConfiguredBaseModel(BaseModel):
    """Base model class for all logger configs.

    Provides common pydantic behavior config to all child models.

    Pydantic Behavior:
        - str_strip_whitespace (True): Automatically strip white spaces from
            all `str` fields
        - validate_assignment (True): Re-validate all field reassignments
        - extra ("forbid"): Reject any unexpected or undeclared fields
    """

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )


# -----------------------------------------------------------------------------
#   Configurations
#   Safe to add additional configs
# -----------------------------------------------------------------------------


class LogLevelConfig:
    """Convert log levels from raw data to an appropriate level.

    Note:
        Should only be inherited by configs that changes a logger's level.
    """

    @field_validator("level", mode="before")
    def parse_log_level(cls, value: str) -> LogLevel:
        return {
            "debug": LogLevel.DEBUG,
            "info": LogLevel.INFO,
            "warning": LogLevel.WARNING,
            "error": LogLevel.ERROR,
            "critical": LogLevel.CRITICAL,
        }[value.lower()]


class ConsoleConfig(ConfiguredBaseModel, LogLevelConfig):
    """Base model for console logger config.

    Inherits From:
        ConfiguredBaseModel: Provides configured pydantic behavior.

    Business Rules:
        - Custom format must contain a placeholder for emitted log's message
    """

    enabled: bool = Field(default=True)
    level: LogLevel = Field(default=LogLevel.INFO)
    fmt: str = (
        "%(asctime)s"
        " | %(levelname)-8s"
        " | %(module)s:%(funcName)s:%(lineno)d"
        " | %(message)s"
    )
    datefmt: str = "%H:%M:%S"

    @model_validator(mode="after")
    def must_have_fmt_and_datefmt(self) -> "ConsoleConfig":
        if not (self.fmt and self.datefmt):
            raise MissingConfigValueError(
                message="The console config is missing format and/or date format",
                err_code=ErrorCode.INF_CFGB_LOOK_522,
            )
        return self


class FileConfig(ConfiguredBaseModel, LogLevelConfig):
    """Base model for file logger config.

    Inherits From:
        ConfiguredBaseModel: Provides configured pydantic behavior.

    Business Rules:
        - Max file size (for file rotation) cannot be larger than 100 MB
        - Backup amount must be within 0-100 range, 0 being no backups
        - Custom format must contain a placeholder for emitted log's message
    """

    enabled: bool = Field(default=True)
    append: bool = Field(default=False)
    output_to: Path = Field(default_factory=lambda: Path(""))
    output_name: str = Field(
        ..., min_length=1, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$"
    )
    level: LogLevel = Field(default=LogLevel.DEBUG)
    max_size_mb: MegaBytes | int = Field(default=Megabyte(10).mb, gt=1, lt=100)
    backup_count: int = Field(default=5, ge=0, le=100)
    # `contextStr` is for dumped JSON with indentation
    # `%(message)s%(contextStr)s` must be together because the JSON formatter
    # automatically appends a colon if context is provided
    fmt: str = (
        "%(asctime)s"
        " | %(levelname)-8s"
        " | %(module)s:%(funcName)s:%(lineno)d"
        " | %(message)s%(contextStr)s"
    )
    datefmt: str = "%H:%M:%S"

    # `output_to` from JSON is str
    @field_validator("output_to", mode="before")
    def parse_output_to(cls, value: str) -> Path:
        return Path(value) if not isinstance(value, Path) else value

    # `max_size_mb` from JSON is int
    @field_validator("max_size_mb", mode="before")
    def parse_file_size_mb(cls, value: int) -> MegaBytes:
        return Megabyte(value).mb if not isinstance(value, MegaBytes) else value

    @model_validator(mode="after")
    def must_have_fmt_and_datefmt(self) -> "FileConfig":
        if not (self.fmt and self.datefmt):
            raise MissingConfigValueError(
                message="The file config is missing format and/or date format",
                err_code=ErrorCode.INF_CFGB_LOOK_522,
            )
        return self

    @model_validator(mode="after")
    def must_have_output_to(self) -> "FileConfig":
        if not self.output_to:
            raise MissingConfigValueError(
                message="The file config is missing the output path",
                err_code=ErrorCode.INF_CFGB_LOOK_523,
            )
        return self


class AsyncConfig(ConfiguredBaseModel):
    """Base model for logger's async config.

    Inherits From:
        ConfiguredBaseModel: Provides configured pydantic behavior.
    """

    enabled: bool = False
    # For database and caching
    # This comment is from future me: wtf do you mean?
    queue_size: int = Field(default=1000, gt=0)
    timeout: float = Field(default=1.0, gt=0.0, le=60.0)


class SecurityConfig(ConfiguredBaseModel):
    """Base model for logger's security config.

    Inherits From:
        ConfiguredBaseModel: Provides configured pydantic behavior.
    """

    enabled: bool = True
    sanitize_sensitive_data: bool = True


class FilterConfig(ConfiguredBaseModel):
    """Base model for logger's filter config.

    Inherits From:
        ConfiguredBaseModel: Provides configured pydantic behavior.
    """

    enabled: bool = False
    rate_limit: Optional[int] = Field(default=None, gt=0)
    include_patterns: List[str] = Field(default_factory=List)
    exclude_patterns: List[str] = Field(default_factory=List)


# -----------------------------------------------------------------------------
#   Top-level configuration
#   Safe to add additional configs
# -----------------------------------------------------------------------------


class LoggerConfig(BaseConfig, ConfiguredBaseModel):
    """Base model for logger config.

    Inherits From:
        ConfiguredBaseModel: Provides configured pydantic behavior.

    Business Rules:
        - Either of the console and file must be enabled
    """

    console: ConsoleConfig = Field(default_factory=ConsoleConfig)
    file: FileConfig = Field(default_factory=FileConfig)
    async_: AsyncConfig = Field(default_factory=AsyncConfig, alias="async")
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    filters: FilterConfig = Field(default_factory=FilterConfig)

    @model_validator(mode="after")
    def at_least_one_enabled(self) -> "LoggerConfig":
        if not (self.console.enabled or self.file.enabled):
            raise MissingConfigValueError(
                message="The logger config is missing file and/or console handler",
                err_code=ErrorCode.INF_CFGB_LOOK_524,
            )
        return self
