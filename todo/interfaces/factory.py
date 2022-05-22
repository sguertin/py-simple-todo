from abc import ABCMeta, abstractmethod
from logging import Logger

from todo.constants import LogLevel
from todo.models.todo_file import TodoItem, TodoList
from todo.views.list_view import ManageItemView, ListView


class IManageItemViewFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create") and callable(subclass.create)
        ) or NotImplemented

    @abstractmethod
    def create(
        self, todo_list: TodoList, todo_item: TodoItem, edit: bool = False
    ) -> ManageItemView:
        """Creates a view to create/edit a todo item

        Args:
            todo_list (TodoList): The todo list
            todo_item (TodoItem): the todo item
            edit (bool, optional): True if this is an edit. Defaults to False.

        Returns:
            ManageTodoItemView: The constructed view
        """
        raise NotImplementedError()


class IItemViewFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create") and callable(subclass.create)
        ) or NotImplemented

    @abstractmethod
    def create(self, todo_item: TodoItem) -> list:
        """Generate a TodoItemView for a todo item

        Args:
            todo_item (TodoItem): The todo_item to display

        Returns:
            list: a list UI Elements for the Todo Item
        """
        raise NotImplementedError()


class IListViewFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create") and callable(subclass.create)
        ) or NotImplemented

    @abstractmethod
    def create(self, todo_list: TodoList) -> ListView:
        """Creates an instance of the TodoListView for a given todo list

        Args:
            todo_list (TodoList): The todo list

        Returns:
            TodoListView: The constructed view
        """
        raise NotImplementedError()


class ILoggingFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "get_logger") and callable(subclass.get_logger))
            and (hasattr(subclass, "update_level") and callable(subclass.update_level))
            or NotImplemented
        )

    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        """Retrieves a configured instance of the Logger class with the appropriate name

        Args:
            name (str): The name for the logger

        Returns:
            Logger: The configured logger
        """
        raise NotImplementedError()

    @abstractmethod
    def update_level(self, log_level: LogLevel):
        """Updates the default log level for the factory

        Args:
            log_level (LogLevel): The new log level to be used as the default

        """
        raise NotImplementedError()
