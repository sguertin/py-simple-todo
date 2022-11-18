from datetime import datetime
import logging
import logging.config
from logging import Logger, FileHandler

from rich.logging import RichHandler

from todo_list.constants import LogLevel, LOGS_DIRECTORY
from todo_list.interfaces.factory import ILoggingFactory


class LoggingFactory(ILoggingFactory):
    _log_level: LogLevel

    def __init__(self, log_level: LogLevel):
        self._log_level = log_level
        time_stamp = datetime.now().strftime("%Y-%m-%d")
        log_file_path = LOGS_DIRECTORY / f"SimpleTodoList-{time_stamp}.log"
        logging.basicConfig(
            datefmt="[%Y-%m-%d %H:%M:%S]",
            format="%(name)-20s - %(message)s",
            handlers=[
                RichHandler(rich_tracebacks=True),
                FileHandler(log_file_path, "w+"),
            ],
            level=LogLevel.NOTSET,
        )

    def update_level(self, log_Level: LogLevel):
        self._log_level = log_Level

    def get_logger(self, name: str) -> Logger:
        log = logging.getLogger(name)
        log.setLevel(self._log_level)
        return log


class TestLoggingFactory(LoggingFactory):
    def __init__(self, log_level: LogLevel = LogLevel.INFO):
        self._log_level = log_level
        logging.basicConfig(
            datefmt="[%Y-%m-%d %H:%M:%S]",
            format="%(name)-20s - %(message)s",
            handlers=[
                RichHandler(rich_tracebacks=True),
            ],
            level=LogLevel.NOTSET,
        )
