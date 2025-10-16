import asyncio
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Optional, Self

import aiofiles
import aiofiles.os

from models.todo import TodoItem, EMPTY
from providers.settings import SettingsProvider

DEFAULT_TEXT = "Get Something Done!"
class TodoItemService:
    settings_provider: SettingsProvider
    todo_items: list[TodoItem]
    _lock = Lock()

    @property
    def working_directory(self) -> Path:
        return self.settings_provider.settings.default_directory

    @classmethod
    async def _new(cls) -> Self:
        if hasattr(cls, "instance"):
            return cls.instance        
        todo_service = cls()
        todo_service.settings_provider = SettingsProvider()
        await todo_service.load_list()
        return todo_service

    def __new__(cls):
        with cls._lock:
            if not hasattr(cls, "instance"):
                cls.instance = super(TodoItemService, cls).__new__(cls)
        return cls.instance

    async def set_working_directory(self, new_working_directory: Path) -> None:
        if new_working_directory.is_file():
            raise NotADirectoryError(f"new_working_directory cannot be a file!")
        elif not new_working_directory.exists():
            raise FileNotFoundError(f"'{new_working_directory}' does not exist!")
        self.settings_provider.settings.default_directory = new_working_directory
        await self.settings_provider.save_settings(self.settings_provider.settings)

    async def load_list(self) -> None:
        todo_files = [
            entry
            for entry in self.working_directory.iterdir()
            if entry.is_file() and entry.suffix.lower() == ".todo"
        ]
        if not todo_files:
            self.todo_items = [await self.new_todo(DEFAULT_TEXT)]            
        else:
            self.todo_items = [await self.read_file(file) for file in todo_files]
        

    async def new_todo(
        self,
        title: str,
        description: str = EMPTY,
        category: str = EMPTY,
        due_date: Optional[datetime] = None,
    ) -> TodoItem:
        with self._lock:
            if not any(self.todo_items):
                new_id = 1
            else:
                new_id = max([todo_item.id for todo_item in self.todo_items]) + 1 
            file_path = self.working_directory / Path(f"{new_id}.todo")
            new_item = TodoItem(
                new_id,
                title,
                description,
                category,
                due_date=due_date,
                file_path=file_path,
            )
            self.todo_items.append(new_item)
            await self.save_todo(new_item)
            return new_item
    
    async def save_todo(self, todo_item: TodoItem):
        with self._lock:
            if todo_item not in self.todo_items:
                self.todo_items.append(todo_item)
            async with aiofiles.open(todo_item.file_path, 'w+') as f:
                await f.write(todo_item.to_json())
    
    async def delete_todo(self, todo_item: TodoItem):
        with self._lock:
            if todo_item in self.todo_items:
                self.todo_items.remove(todo_item)
            if todo_item.file_path is not None:
                await aiofiles.os.remove(todo_item.file_path)
    
    @staticmethod
    async def read_file(file_path: Path) -> TodoItem:
        async with aiofiles.open(file_path, 'r+') as f:
            return TodoItem.from_json(await f.read())

asyncio.run(TodoItemService._new())