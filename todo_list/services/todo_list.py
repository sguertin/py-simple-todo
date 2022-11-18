from datetime import datetime
from logging import Logger
from typing import Optional
from uuid import UUID

import PySimpleGUI as sg

from todo_list.constants import UiKeys
from todo_list.interfaces.factory import (
    IListViewFactory,
    IManageItemViewFactory,
    ILoggingFactory,
)
from todo_list.interfaces.todo_file import IFileService
from todo_list.interfaces.todo_list import IListUiService
from todo_list.models.todo import TodoItem, TodoList


def extract_id(event, key) -> UUID:
    return UUID(str(event).replace(str(key), ""))


class ListUiService(IListUiService):
    log: Logger
    file_service: IFileService
    manage_view_factory: IManageItemViewFactory
    list_view_factory: IListViewFactory

    def __init__(
        self,
        log_factory: ILoggingFactory,
        file_service: IFileService,
        list_view_factory: IListViewFactory,
        manage_view_factory: IManageItemViewFactory,
    ):
        self.manage_view_factory = manage_view_factory
        self.log = log_factory.get_logger("TodoListView")
        self.list_view_factory = list_view_factory
        self.file_service = file_service

    def run(self) -> None:
        self.log.debug("Starting TodoListView")
        while self._run():
            self.log.debug("Refreshing TodoListView")
        self.log.debug("Closing TodoListView")

    def _run(self) -> bool:
        todo_list = self.file_service.load()
        window = self.list_view_factory.create(todo_list)
        while True:
            event, values = window.read()
            self.log.debug("Event %s received", event)
            if event == UiKeys.REFRESH:
                window.close()
                return True
            elif event == UiKeys.NEW:
                window.close()
                self.manage_item(todo_list)
                return True
            elif str(event).startswith(UiKeys.EDIT):
                id = extract_id(event, UiKeys.EDIT)
                window.close()
                self.manage_item(todo_list, todo_list.todo_dict[id])
                return True
            elif str(event).startswith(UiKeys.COMPLETED):
                id = extract_id(event, UiKeys.COMPLETED)
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

    def manage_item(self, todo_list: TodoList, todo_item: Optional[TodoItem] = None):
        new = False
        if todo_item is None:
            todo_item = TodoItem()
            new = True
        view = self.manage_view_factory.create(todo_list, todo_item, new)
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
