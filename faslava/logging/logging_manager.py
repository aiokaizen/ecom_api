import os
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler#, StreamHandler
from typing import Optional, Dict


class LoggingManager:
    def __init__(self, name: str = "app_logger", default_level: int = logging.INFO):
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

    # def add_console_handler(self, level: Optional[int] = logging.INFO):
    #     """Add a console (stdout) logging handler."""
    #     handler = StreamHandler()
    #     handler.setLevel(level)
    #     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    #     handler.setFormatter(formatter)
    #     self.logger.addHandler(handler)
    #     self.handlers["console"] = handler

    def add_file_handler(self, filepath: str, level: int = logging.INFO, max_bytes: int = 10485760, backup_count: int = 5):
        """Add a rotating file logging handler."""
        handler = RotatingFileHandler(filepath, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.handlers["file"] = handler

    def add_email_handler(self, mailhost: str, fromaddr: str, toaddrs: list, subject: str, credentials: Optional[tuple] = None, level: int = logging.ERROR):
        """Add an email logging handler."""
        handler = SMTPHandler(mailhost=mailhost, fromaddr=fromaddr, toaddrs=toaddrs, subject=subject, credentials=credentials)
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.handlers["email"] = handler

    def remove_handler(self, handler_name: str):
        """Remove a handler by name."""
        if handler_name in self.handlers:
            handler = self.handlers.pop(handler_name)
            self.logger.removeHandler(handler)

    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger


_log_manager = LoggingManager(name="default_logger", default_level=logging.DEBUG)

# Add console handler
# log_manager.add_console_handler(level=logging.DEBUG)

# Add file handler
_log_manager.add_file_handler(filepath="faslava.log", level=logging.INFO)

# Add email handler (example)
# _log_manager.add_email_handler(
#     mailhost="smtp.example.com",
#     fromaddr="error@example.com",
#     toaddrs=["admin@example.com"],
#     subject="Application Error",
#     credentials=("username", "password"),
#     level=logging.ERROR
# )

# Add other handlers

logger = _log_manager.get_logger()
