from ....shared.logger.log_levels import LogLevel
from ..models.logger_config import LoggerConfig
from ..services.base_builder import BaseConfigBuilder


class LoggerConfigBuilder(BaseConfigBuilder[LoggerConfig]):
    """Config builder implementation for logger.

    Inherits From:
        `BaseConfigBuilder[LoggerConfig]`: Specializes the generic config
        builder for logger specifically. All type parameters and returns
        are resolved to `LoggerConfig` type.

    This implementation provides public methods that allow for default configs,
    read from a JSON config file, to be overridden before building (Getting
    the config data).

    Public Methods:
        - with_console_level(level): Change the log level for console logs
        - with_file_level(level): Change the log level for file logs

    Type Resolution:
        - `.reset()`: Becomes `.reset() -> BaseConfigBuilder[LoggerConfig]`;
            Resets internal config to its original default state
        - `.build()`: Becomes `.build() -> LoggerConfig`;
            Finalizes and returns current config
    """

    def with_console_level(self, level: LogLevel) -> "LoggerConfigBuilder":
        """Overrides default config of the logger's console level.

        Updates the log level config for logging to console.

        Args:
            level: The level to change to. Choices are:
            `"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"`

        Returns:
            Updated config instance; not yet built.
        """

        # Validate to avoid unwanted values
        console = self._validated_copy(self._current_config.console, level=level)
        self._current_config = self._current_config.model_copy(
            update={"console": console}
        )
        return self

    def with_file_level(self, level: LogLevel) -> "LoggerConfigBuilder":
        """Overrides default config of logger's file level.

        Updates the log level config for logging to file.

        Args:
            level: The level to change to. Choices are:
            `"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"`

        Returns:
            Updated config instance; not yet built.
        """

        # Validate to avoid unwanted values
        file = self._validated_copy(self._current_config.file, level=level)
        self._current_config = self._current_config.model_copy(update={"file": file})
        return self
