from abc import ABCMeta, abstractmethod
from typing import Optional

from todo.models.todo_file import TodoItem, TodoList


class ITodoListUiService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "run") and callable(subclass.run))
            and (hasattr(subclass, "add_item") and callable(subclass.add_item))
            and (
                hasattr(subclass, "manage_todo_item")
                and callable(subclass.manage_todo_item)
            )
            or NotImplemented
        )

    @abstractmethod
    def run(self) -> None:
        """Runs the main UI loop for the Todo List"""
        raise NotImplementedError()

    def add_item(self, todo_list: TodoList, new_item: TodoItem) -> None:
        """Add a new todo item to the list and save the update

        Args:
            todo_list (TodoList): The current list of todo items
            new_item (TodoItem): The new todo item to be added

        Raises:
            Exception: Raised if a Todo Item with the same Id already exists in the list
        """
        raise NotImplementedError()

    def manage_todo_item(
        self, todo_list: TodoList, todo_item: Optional[TodoItem] = None
    ):
        """Launches a UI for creating or editing a Todo Item

        Args:
            todo_list (TodoList): The current list of todo items
            todo_item (Optional[TodoItem], optional): The Todo Item to edit. Defaults to None which creates a new item.

        """
        raise NotImplementedError()
