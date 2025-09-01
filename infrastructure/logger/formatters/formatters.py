import json
from datetime import datetime
from logging import Formatter, LogRecord, makeLogRecord

# -----------------------------------------------------------------------------
#   Formatters
# -----------------------------------------------------------------------------


class JSONFormatter(Formatter):
    """Custom formatter for a fully structured JSON logging.

    This formatter constructs all data into a JSON format.

    Methods:
        format: Formats emitted log to a JSON struct
    """

    def format(self, record: LogRecord) -> str:
        """Formats recorded recorded log to a JSON struct.

        Args:
            record: A `LogRecord` containing the records of data
                    an emitted log carries

        timestamp:  Datetime format of when log was logged
                    or created. Initially a UNIX timestamp.
        level:      Name of the logging level.
        logger:     Name of the logger that emitted the
                    record.
        service:    A custom added filter to get service
                    name of the logger.
        message:    Formatted log message.
        module:     Name of the module where the log was
                    emitted. A filename without the
                    extension.
        function:   Name of the function containing the
                    the logging call.
        line:       Line number in source code where
                    the log was triggered.

        Returns:
            The formatted record as text.
        """
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "service": getattr(record, "service", "unknown"),
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        log_entry.update(getattr(record, "extra_data", {}))

        return json.dumps(log_entry, default=str)


class ContextJSONFormatter(Formatter):
    """Custom logger formatter that appends structured context as
       indented JSON.

    This formatter constructs only the context into a JSON format.

    Methods:
        format: Formats emitted log context to a JSON struct
    """

    def format(self, record: LogRecord) -> str:
        """Override format to add custom formatter algorithm.

        Args:
            record: A `LogRecord` containing the records of data
                    an emitted log carries

        standard_attrs: A set of standard attributes that should
                        not be a part of the emitted log.
        redundant_keys: Skips redundant keys from the log record
                        that already appear on every
        excluded_keys:  A union of sets to exclude from the
                        context.
        context:        A raw dict that contains the key-values
                        to be formatted to a str in JSON struct.
        contextStr:     The formatted JSON context as str.

        Returns:
            The formatted specified record as text.
        """

        # Extract standard fields to exclude
        standard_attrs = set(makeLogRecord({}).__dict__.keys())

        # Exclude redundant keys
        redundant_keys = {"contextStr", "message", "asctime", "service"}

        excluded_keys = standard_attrs | redundant_keys

        # Extract custom context from `record.__dict__`
        context = {k: v for k, v in record.__dict__.items() if k not in excluded_keys}

        record.contextStr = f":\n{json.dumps(context, indent=4)}" if context else ""
        return super().format(record)
