from json import JSONDecodeError
from logging import Logger

from todo.constants import TODO_FILE
from todo.interfaces.log_factory import ILoggingFactory
from todo.interfaces.todofile import ITodoFileService
from todo.models.todofile import TodoList


class TodoFileService(ITodoFileService):
    log: Logger

    def __init__(self, log_factory: ILoggingFactory):
        self.log = log_factory.get_logger("TodoFileService")

    def load_todo_list(self) -> TodoList:
        try:
            if not TODO_FILE.exists():
                todo_list = TodoList()
            else:
                with open(TODO_FILE, "r") as f:
                    todo_list = TodoList.from_json(f.read())
        except JSONDecodeError as ex:
            self.log.exception(ex)
            todo_list = TodoList()
        return todo_list
    
    def save_todo_list(self, todo_list: TodoList) -> None:
        with open(TODO_FILE, "w+") as f:
            f.write(todo_list.to_json())


