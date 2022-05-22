from enum import IntEnum, Enum
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from os import getenv
from pathlib import Path

WORKING_DIR: Path = Path(getenv("USERPROFILE", getenv("HOME")), "TimeTracking")
LOGS_DIRECTORY: Path = Path(WORKING_DIR, "Logs")
TODO_FILE: Path = Path(WORKING_DIR, "TodoList.json")
ISSUES_LIST: Path = Path(WORKING_DIR, "issues.json")
DELETED_ISSUES_LIST: Path = Path(WORKING_DIR, "deletedIssues.json")
SETTINGS_FILE: Path = Path(WORKING_DIR, "settings.json")

HOUR_RANGE: range = range(24)
MINUTE_RANGE: range = range(60)


class LogLevel(IntEnum):
    NOTSET = NOTSET
    CRITICAL = CRITICAL
    ERROR = ERROR
    WARNING = WARNING
    INFO = INFO
    DEBUG = DEBUG


class UiKeys(Enum):
    CANCEL = "Cancel"
    CATEGORY = "-CATEGORY-"
    COMPLETED = "COMPLETED-"
    DESCRIPTION = "-DESCRIPTION-"
    DUE_DATE = "-DUE-DATE-"
    EDIT = "EDIT-"
    NEW = "-NEW-"
    QUIT = "-QUIT-"
    REFRESH = "-REFRESH-"
    SAVE = "-SAVE-"
    SET_CATEGORY = "-SET-CATEGORY-"
    SUBMIT = "Submit"
    TIMEOUT = "-TIMEOUT-"
    TITLE = "-TITLE-"

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, value: str) -> bool:
        return str(self.value) == value
