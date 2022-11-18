from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import config, DataClassJsonMixin, LetterCase

from todo_list.constants import LogLevel


@dataclass
class TimeOfDay(DataClassJsonMixin):
    hour: int
    minute: int

    def __str__(self):
        return self.to_json()


@dataclass
class Settings(DataClassJsonMixin):
    last_updated: datetime
    log_level: LogLevel
    reminder_times: list[TimeOfDay]
    theme: str

    def __init__(self):
        self.dataclass_json_config = config(letter_case=LetterCase.CAMEL)
        self.last_updated = datetime.now()
        self.log_level = LogLevel.INFO
        self.reminder_times = [TimeOfDay(8, 30)]
        self.theme = "DarkBlue3"

    def __str__(self):
        return self.to_json()
