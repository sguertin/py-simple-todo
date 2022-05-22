from dataclasses import dataclass
from datetime import datetime, time
from uuid import uuid4, UUID
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
    id: UUID
    title: str
    description: str
    due_date: datetime
    category: str
    completed: bool
    completed_date: datetime
    created: datetime
    updated: datetime

    def __init__(
        self,
        title: str = "",
        description: str = "",
        category: str = "Uncategorized",
        due_date: datetime = None,
    ):
        today = datetime.today()
        self.id = uuid4()
        self.title = title
        self.description = description
        self.category = category
        self.completed = False
        self.created = today
        self.due_date = due_date
        self.updated = today


@dataclass
class TodoList(DataClassJsonMixin):
    created: datetime
    updated: datetime
    todo_items: list[TodoItem]

    @property
    def categories(self) -> list[str]:
        return [todo_item.category for todo_item in self.todo_items]

    @property
    def todo_dict(self) -> dict[UUID, TodoItem]:
        return {item.id: item for item in self.todo_items}

    def __init__(self):
        today = datetime.today()
        self.created = today
        self.updated = today
        self.todo_items = []
