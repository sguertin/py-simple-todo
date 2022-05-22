from datetime import datetime, timedelta

import PySimpleGUI as sg

from todo.constants import UiKeys
from todo.interfaces.factory import (
    IManageItemViewFactory,
    IItemViewFactory,
    IListViewFactory,
)
from todo.models.todo_file import TodoItem, TodoList
from todo.views.list_view import ManageItemView, ItemView, ListView


class ManageItemViewFactory(IManageItemViewFactory):
    def create(
        self, todo_list: TodoList, todo_item: TodoItem, edit: bool = False
    ) -> ManageItemView:
        if edit:
            title = "Edit Todo Item"
        else:
            title = "Create New Todo Item"

        category_field = sg.Input(
            todo_item.category,
            default_value=todo_item.category,
            key=UiKeys.CATEGORY,
        )
        return ManageItemView(
            title,
            [
                [sg.T("Title: "), sg.Input(todo_item.title, key=UiKeys.TITLE)],
                [
                    sg.T("Description: "),
                    sg.Input(todo_item.description, key=UiKeys.DESCRIPTION),
                ],
                [
                    sg.T("Category: "),
                    category_field,
                    sg.Combo(
                        todo_list.categories,
                        enable_events=True,
                        key=UiKeys.SET_CATEGORY,
                    ),
                ],
                [
                    sg.T("Due Date: "),
                    sg.Input(todo_item.due_date, key=UiKeys.DUE_DATE, readonly=True),
                    sg.CalendarButton("Due Date for Todo Item", target=UiKeys.DUE_DATE),
                ],
                [sg.Submit("Save"), sg.Cancel()],
            ],
            category_field,
        )


class ItemViewFactory(IItemViewFactory):
    def create(self, todo_item: TodoItem) -> ItemView:
        return ItemView(
            [
                sg.Checkbox(
                    "Completed",
                    default=todo_item.completed,
                    enable_events=True,
                    key=f"{UiKeys.COMPLETED}{todo_item.id}",
                ),
                sg.T(todo_item.description),
                sg.Button(
                    "Edit", key=f"{UiKeys.EDIT}{todo_item.id}", metadata=todo_item
                ),
            ]
        )


class ListViewFactory(IListViewFactory):
    todo_item_factory: IItemViewFactory

    def __init__(self, todo_item_factory: IItemViewFactory):
        self.todo_item_factory = todo_item_factory

    def create(self, todo_list: TodoList) -> ListView:
        now = datetime.now()
        tomorrow = datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(
            days=1
        )
        todo_items = [
            self.todo_item_factory.create(todo_item)
            for todo_item in todo_list.todo_items
            if not todo_item.completed
            or (todo_item.completed_date < tomorrow and todo_item.completed)
        ]
        return ListView(
            "My Todo List",
            [
                [sg.T(f"Current Todo Items")],
                *todo_items,
                [
                    sg.Button("New Item", key=UiKeys.NEW),
                    sg.Button("Refresh", key=UiKeys.REFRESH),
                    sg.Button("Quit", key=UiKeys.QUIT),
                ],
            ],
        )
