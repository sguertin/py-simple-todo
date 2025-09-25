from asyncio import run
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Optional, Self

from models.todo import TodoItem, EMPTY
from providers.settings import SettingsProvider


class TodoItemService:
    settings: SettingsProvider
    todo_items: list[TodoItem]
    _lock = Lock()
    _file_lock = Lock()

    @property
    def working_directory(self) -> Path:
        return self.settings.get_settings().default_directory

    @classmethod
    async def _new(cls) -> Self:
        if hasattr(cls, "instance"):
            return cls.instance
        todo_service = cls()
        await todo_service.load_list()
        return todo_service

    def __new__(cls):
        with cls._lock:
            if not hasattr(cls, "instance"):
                cls.instance = super(TodoItemService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.settings = SettingsProvider()

    async def set_working_directory(self, new_working_directory: Path) -> None:
        if new_working_directory.is_file():
            raise NotADirectoryError(f"new_working_directory cannot be a file!")
        elif not new_working_directory.exists():
            raise FileNotFoundError(f"'{new_working_directory}' does not exist!")
        settings = self.settings.get_settings()
        settings.default_directory = new_working_directory
        await self.settings.save_settings(settings)

    async def load_list(self) -> None:
        todo_files = [
            entry
            for entry in self.working_directory.iterdir()
            if entry.is_file() and entry.suffix.lower() == ".todo"
        ]

        self.todo_items = [await TodoItem.read_file(file) for file in todo_files]

    async def new_todo(
        self,
        title: str,
        description: str = EMPTY,
        category: str = EMPTY,
        due_date: Optional[datetime] = None,
    ) -> None:
        with self._lock:
            if not any(self.todo_items):
                new_id = 1
            else:
                new_id = max([todo_item.id for todo_item in self.todo_items])
            file_path = self.working_directory / Path(f"{new_id}-{title}.todo")
            new_item = TodoItem(
                new_id,
                title,
                description,
                category,
                due_date=due_date,
                file_path=file_path,
            )
            self.todo_items.append(new_item)
            await new_item.write()

run(TodoItemService._new())