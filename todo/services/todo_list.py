from datetime import datetime, timedelta
from logging import Logger
from typing import Optional
from uuid import UUID

import PySimpleGUI as sg

from todo.constants import UiKeys
from todo.interfaces.log_factory import ILoggingFactory
from todo.interfaces.todo_file import ITodoFileService
from todo.interfaces.todo_list import ITodoListUiService
from todo.models.todo_file import TodoItem, TodoList
from todo.views.todo_list import ManageTodoItemViewFactory, TodoListViewFactory


class TodoListUiService(ITodoListUiService):
    log: Logger
    file_service: ITodoFileService

    def __init__(self, log_factory: ILoggingFactory, file_service: ITodoFileService):
        self.log = log_factory.get_logger("TodoListView")
        self.file_service = file_service

    def run(self) -> None:
        self.log.info("Starting TodoListView")
        while self._run():
            self.log.debug("Refreshing TodoListView")
        self.log.info("Closing TodoListView")

    def _run(self) -> bool:
        todo_list = self.file_service.load()
        window = TodoListViewFactory.create(todo_list)
        while True:
            event, values = window.read()
            self.log.debug("Event %s received", event)
            if event == UiKeys.REFRESH:
                window.close()
                return True
            elif event == UiKeys.NEW:
                window.close()
                self.manage_todo_item()
                return True
            elif str(event).startswith(UiKeys.EDIT):
                id = UUID(str(event).replace(UiKeys.EDIT.value, ""))
                window.close()
                self.manage_todo_item(todo_list.todo_dict[id])
                return True
            elif str(event).startswith(UiKeys.COMPLETED):
                id = UUID(str(event).replace(UiKeys.COMPLETED.value, ""))
                todo_item = todo_list.todo_dict[id]
                todo_item.completed = values[event]
                self.file_service.save(todo_list)
            elif event in (sg.WIN_CLOSED, UiKeys.QUIT):
                return False
            window.refresh()

    def add_item(self, todo_list: TodoList, new_item: TodoItem) -> None:
        if new_item.id not in todo_list.todo_dict.keys():
            self.updated = datetime.now()
            todo_list.todo_items.append(new_item)
        else:
            raise Exception("Todo Item already exists!")

    def manage_todo_item(
        self, todo_list: TodoList, todo_item: Optional[TodoItem] = None
    ):
        new = False
        if todo_item is None:
            todo_item = TodoItem()
            new = True
        view = ManageTodoItemViewFactory.create(todo_list, todo_item, new)
        while True:
            event, values = view.read()
            if event == UiKeys.SET_CATEGORY:
                view.update_category(values[UiKeys.SET_CATEGORY])
            if event == UiKeys.SUBMIT:
                todo_item.title = values[UiKeys.TITLE]
                todo_item.description = values[UiKeys.DESCRIPTION]
                todo_item.category = values[UiKeys.CATEGORY]
                todo_item.due_date = values[UiKeys.DUE_DATE]
                todo_item.updated = datetime.now()
                try:
                    if new:
                        self.add_item(todo_list, todo_item)
                except Exception as e:
                    self.log.exception(e)
                self.file_service.save(todo_list)
            if event in (UiKeys.SUBMIT, UiKeys.CANCEL):
                view.close()
                break
