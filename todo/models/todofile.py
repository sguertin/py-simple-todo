from dataclasses import dataclass
from datetime import datetime, time

from dataclasses_json import DataClassJsonMixin


@dataclass
class TimeEntry(DataClassJsonMixin):
    start_time: time
    end_time: time
    entry: str

    def __init__(self, start_time: datetime, end_time: datetime, entry: str):
        self.start_time = start_time.time()
        self.end_time = end_time.time()
        self.entry = entry

@dataclass
class TodoItem(DataClassJsonMixin):
    title: str
    description: str
    created: datetime 
    updated: datetime
    completed: bool
    category: str
    due_date: datetime

    def __init__(self, title: str, description: str, category: str = "Uncategorized", due_date: datetime = None):
        today = datetime.today()
        self.title = title
        self.description = description
        self.category = category
        self.completed = False
        self.created = today
        self.due_date = due_date
        self.updated = today

@dataclass
class TodoList(DataClassJsonMixin):
    file_name: str = "TodoList.json"
    created: datetime = datetime.today()
    updated: datetime = datetime.today()
    todo_items: list[TodoItem] = []
    def __init__(self):
        today = datetime.today()
        self.created = today
        self.updated = today
        self.file_name = "TodoList.json"

@dataclass
class TimeDayLog(DataClassJsonMixin):
    log_date: datetime
    file_name: str
    time_entries: list[TimeEntry]

    def __init__(self):
        today = datetime.today()
        self.log_date = today
        self.time_entries = []
        self.file_name = f"TimeTracking-{today.year}-{today.month}-{today.day}.log"
