import os
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from typing import Dict


class LoggingManager:
    def __init__(
        self,
        name: str = "faslava.logging.LoggingManager",
        default_level: int = logging.INFO,
    ):
        """
        Initialize the LoggingManager with a specific logger name.

        Args:
            name (str): Name of the logger.
            default_level (int): Default logging level.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(default_level)
        self.handlers: Dict[str, logging.Handler] = {}

        logs_dir = "logging"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

    def add_console_handler(self, level: int = logging.INFO):
        """Add a console (stdout) logging handler."""
        handler = StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.handlers["console"] = handler

    def add_file_handler(
        self,
        filepath: str,
        level: int = logging.INFO,
        max_bytes: int = 10485760,
        backup_count: int = 5,
    ):
        """Add a rotating file logging handler."""
        handler = RotatingFileHandler(
            filepath, maxBytes=max_bytes, backupCount=backup_count
        )
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.handlers["file"] = handler

    def remove_handler(self, handler_name: str):
        """Remove a handler by name."""
        if handler_name in self.handlers:
            handler = self.handlers.pop(handler_name)
            self.logger.removeHandler(handler)

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger


_log_manager = LoggingManager(default_level=logging.DEBUG)

# Add console handler
_log_manager.add_console_handler(level=logging.DEBUG)

# Add file handler
_log_manager.add_file_handler(filepath="logging/faslava.log", level=logging.INFO)


logger = _log_manager.get_logger()
