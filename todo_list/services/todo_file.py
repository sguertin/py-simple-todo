from json import JSONDecodeError
from logging import Logger

from todo_list.constants import TODO_FILE
from todo_list.decorators import fire_and_forget
from todo_list.interfaces.factory import ILoggingFactory
from todo_list.interfaces.todo_file import IFileService
from todo_list.models.todo import TodoList


class FileService(IFileService):
    log: Logger

    def __init__(self, log_factory: ILoggingFactory):
        self.log = log_factory.get_logger("TodoFileService")

    def load(self) -> TodoList:
        try:
            if not TODO_FILE.exists():
                todo_list = TodoList()
                self.save(todo_list)
            else:
                with open(TODO_FILE, "r") as f:
                    todo_list = TodoList.from_json(f.read())
        except JSONDecodeError as ex:
            self.log.exception(ex)
            todo_list = TodoList()
        return todo_list

    @fire_and_forget
    def save(self, todo_list: TodoList) -> None:
        try:
            with open(TODO_FILE, "w+") as f:
                f.write(todo_list.to_json())
            self.log.debug("Todo List Saved Successfully")
        except Exception as e:
            self.log.exception(e)
