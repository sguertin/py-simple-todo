from asyncio import run
from typing import Any

import FreeSimpleGUI as sg
from rich import print

from services.todo import TodoItemService
from models.todo import TodoItem
from constants.events import ADD_EVENT, SAVE_EVENT, EDIT_EVENT, DELETE_EVENT, EXIT_EVENT
from constants.icons import CALENDAR_ICON, DELETE_ICON, EDIT_ICON, SAVE_ICON
from constants.keys import CATEGORY_KEY, DESCRIPTION_KEY, DUE_DATE_KEY, NOTES_KEY

TODO_LIST_ID = "-TODO LIST-"
ROW_ID = "-ROW-"

SPACER_SIZE = (8, 1)
LARGE_FIELD_SIZE = (31, 17)
SMALL_COLUMN_SIZE = (4, 1)
MEDIUM_COLUMN_SIZE = (25, 1)
LARGE_COLUMN_SIZE = (55, 1)

COLUMN_FONT_CONFIG = "Delugia 12"
DEFAULT_FONT_CONFIG = "Delugia 15"
DEFAULT_TEXT = "Get Something Done!"


class TodoEditor:
    todo_service: TodoItemService
    window: sg.Window

    def __init__(self):
        self.todo_service = TodoItemService()

    def make_todo_editor(self, todo_item: TodoItem) -> sg.Window:
        due_date = (None, None, None)
        due_date_text = ""
        if todo_item.due_date is not None:
            due_date = (
                todo_item.due_date.month,
                todo_item.due_date.day,
                todo_item.due_date.year,
            )
            due_date_text = todo_item.due_date.strftime("%d/%m/%Y")
        layout = [
            [
                sg.Text("Id:", size=SPACER_SIZE),
                sg.Text(str(todo_item.id), size=SPACER_SIZE),
            ],
            [
                sg.Text("Title:", size=SPACER_SIZE),
                sg.Input(
                    default_text=todo_item.title,
                    key=("-Title-", todo_item),
                    do_not_clear=False,
                    size=(31, 1),
                ),
            ],
            [
                sg.Text("Due Date:", size=SPACER_SIZE),
                sg.Input(
                    default_text=due_date_text,
                    key=(DUE_DATE_KEY, todo_item),
                    do_not_clear=False,
                    size=(28, 1),
                ),
                sg.CalendarButton(CALENDAR_ICON, default_date_m_d_y=due_date),
            ],
            [
                sg.Text("Category:", size=SPACER_SIZE),
                sg.Input(
                    default_text=todo_item.category,
                    key=(CATEGORY_KEY, todo_item),
                    do_not_clear=False,
                    size=(31, 1),
                ),
            ],
            [sg.Text("Description", size=SPACER_SIZE)],
            [
                sg.Text(" ", size=SPACER_SIZE),
                sg.Multiline(
                    size=LARGE_FIELD_SIZE, key=DESCRIPTION_KEY, do_not_clear=False
                ),
            ],
            [sg.Text("Notes", size=SPACER_SIZE)],
            [
                sg.Text(" ", size=SPACER_SIZE),
                sg.Multiline(size=LARGE_FIELD_SIZE, key=NOTES_KEY, do_not_clear=False),
            ],
            [sg.Text(" " * 77), sg.Button(f"{SAVE_ICON} Save", key=SAVE_EVENT)],
        ]
        self.window = sg.Window(
            "Edit Todo Item", layout=layout, finalize=True, metadata=todo_item
        )
        return self.window

    def event_handler(self, event: str, values: dict[str, Any]):
        if event is SAVE_EVENT:
            print(event, values, sep=" ")
            pass  # TODO Need Save Event
        if event is DELETE_EVENT:
            print(event, values, sep=" ")
            pass  # TODO Need delete handler in TodoItemService


class TodoList:
    todo_service: TodoItemService
    window: sg.Window

    def __init__(self):
        self.todo_service = TodoItemService()

    def make_todo_item(self, todo_item: TodoItem) -> list:
        row = [
            sg.pin(
                sg.Column(
                    [
                        [
                            sg.Text(f"{todo_item.id}.", size=SMALL_COLUMN_SIZE),
                            sg.Checkbox(
                                "",
                                key=f"-CHECK-{todo_item.id}-",
                                size=SMALL_COLUMN_SIZE,
                                tooltip="Mark Todo Item as Complete/Incomplete",
                            ),
                            sg.Input(
                                todo_item.title,
                                k=f"-TITLE-{todo_item.id}",
                                size=MEDIUM_COLUMN_SIZE,
                                tooltip="Title of Todo Item",
                            ),
                            sg.Button(
                                EDIT_ICON,
                                border_width=0,
                                k=(EDIT_EVENT, todo_item.id),
                                tooltip="Edit this todo item",
                                size=SMALL_COLUMN_SIZE,
                                metadata=todo_item,
                            ),
                            sg.Button(
                                DELETE_ICON,
                                border_width=0,
                                k=(DELETE_EVENT, todo_item.id),
                                tooltip="Delete this todo item",
                                size=SMALL_COLUMN_SIZE,
                                metadata=todo_item,
                            ),
                        ]
                    ],
                    key=(ROW_ID, todo_item.id),
                    metadata=todo_item,
                )
            )
        ]
        return row

    def get_layout(self, todo_items: list[TodoItem]) -> sg.Window:

        layout = [
            [sg.Text("Todo Items", font=DEFAULT_FONT_CONFIG)],
            [
                sg.Column(
                    [self.make_todo_item(todo_item) for todo_item in todo_items],
                    key=TODO_LIST_ID,
                )
            ],
            [
                sg.Button("New Todo", key=ADD_EVENT, tooltip="Create a new todo item"),
                sg.Button("", key=SAVE_EVENT, tooltip="Save your todo items"),
                sg.Button(EXIT_EVENT, k=EXIT_EVENT, tooltip="Close application"),
            ],
        ]

        right_click_menu = [[""], ["Version", EXIT_EVENT]]

        window = sg.Window(
            "My Todo List",
            layout,
            right_click_menu=right_click_menu,
            use_default_focus=False,
            font=DEFAULT_FONT_CONFIG,
            metadata=1,
        )

        return window
