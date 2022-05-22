from abc import ABCMeta, abstractmethod
from todo.models.todo_file import TodoList


class IFileService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "load") and callable(subclass.load))
            and (hasattr(subclass, "save") and callable(subclass.save))
            or NotImplemented
        )

    @abstractmethod
    def load(self) -> TodoList:
        """Loads the todo list from the working directory, or creates a new one

        Returns:
            TodoList: The current todo list or a new one if a file was not found
        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, todo_list: TodoList) -> None:
        """Saves todo list to the file system in the user's default directory

        Args:
            todo_list (TodoList): the todo list to be saved

        """
        raise NotImplementedError()
