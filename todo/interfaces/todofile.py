from abc import ABCMeta, abstractmethod
from datetime import time, timedelta, datetime
from pathlib import Path
from todo.models.todofile import TimeDayLog, TodoList


class ITodoFileService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (
                hasattr(subclass, "load_todo_list")
                and callable(subclass.load_todo_list)
            )
            and (
                hasattr(subclass, "create_tracking_entry")
                and callable(subclass.create_tracking_entry)
            )
            and (
                hasattr(subclass, "get_last_entry_time")
                and callable(subclass.get_last_entry_time)
            )
            and (hasattr(subclass, "get_time_log") and callable(subclass.get_time_log))
            or NotImplemented
        )

    @abstractmethod
    def load_todo_list(self) -> TodoList:
        """Loads the todo list from the working directory, or creates a new one

        Returns:
            TodoList: The current todo list or a new one if a file was not found
        """
        raise NotImplementedError()

    @abstractmethod
    def save_todo_list(self, todo_list: TodoList) -> None:
        """Saves todo list to the file system in the user's default directory

        Args:
            todo_list (TodoList): the todo list to be saved

        """
        raise NotImplementedError()

