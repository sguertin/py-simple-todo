from asyncio import run
from typing import Any

import FreeSimpleGUI as sg
from rich import print

from registry.handler import HandlerRegistry
from services.todo import TodoItemService
from models.todo import TodoItem
from constants.events import (
    ADD_EVENT,
    SAVE_CLOSE_EVENT,
    SAVE_EVENT,
    EDIT_EVENT,
    DELETE_EVENT,
    EXIT_EVENT,
    VERSION_EVENT,
)
from constants.defaults import DEFAULT_TITLE_TEXT
from constants.gui import (
    DIAGNOSTICS_FIELD_SIZE,
    DUE_DATE_FIELD_SIZE,
    LARGE_FIELD_AREA_SIZE,
    LARGE_FIELD_SIZE,
    MEDIUM_COLUMN_SIZE,
    SMALL_COLUMN_SIZE,
    SPACER_SIZE,
    DEFAULT_FONT_CONFIG,
)
from constants.icons import CALENDAR_ICON, DELETE_ICON, EDIT_ICON, SAVE_ICON, NEW_ICON
from constants.keys import (
    CATEGORY_KEY,
    DESCRIPTION_KEY,
    DUE_DATE_KEY,
    NOTES_KEY,
    TITLE_KEY,
    TODO_LIST_KEY,
    ROW_KEY,
)


class TodoEditorGui:
    todo_service: TodoItemService = TodoItemService()
    _window: sg.Window | None = None
    todo_item: TodoItem

    def __init__(self, todo_item: TodoItem):
        self.todo_item = todo_item

    @property
    def window(self) -> sg.Window:
        if self._window is None:
            self._window = self.get_todo_editor(self.todo_item)
        return self._window

    def get_todo_editor(self, todo_item: TodoItem) -> sg.Window:
        if self._window is not None and todo_item == self.todo_item:
            return self._window
        if todo_item != self.todo_item:
            self.window.close()
            self._window = None
            HandlerRegistry().cancel(self.window)
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
                    key=(TITLE_KEY, todo_item),
                    do_not_clear=False,
                    size=LARGE_FIELD_SIZE,
                ),
            ],
            [
                sg.Text("Due Date:", size=SPACER_SIZE),
                sg.Input(
                    default_text=due_date_text,
                    key=(DUE_DATE_KEY, todo_item),
                    do_not_clear=False,
                    size=DUE_DATE_FIELD_SIZE,
                ),
                sg.CalendarButton(CALENDAR_ICON, default_date_m_d_y=due_date),
            ],
            [
                sg.Text("Category:", size=SPACER_SIZE),
                sg.Input(
                    default_text=todo_item.category,
                    key=(CATEGORY_KEY, todo_item),
                    do_not_clear=False,
                    size=LARGE_FIELD_SIZE,
                ),
            ],
            [sg.Text("Description", size=SPACER_SIZE)],
            [
                sg.Text(" ", size=SPACER_SIZE),
                sg.Multiline(
                    size=LARGE_FIELD_AREA_SIZE, key=DESCRIPTION_KEY, do_not_clear=False
                ),
            ],
            [sg.Text("Notes", size=SPACER_SIZE)],
            [
                sg.Text(" ", size=SPACER_SIZE),
                sg.Multiline(
                    size=LARGE_FIELD_AREA_SIZE, key=NOTES_KEY, do_not_clear=False
                ),
            ],
            [
                sg.Text(" " * 77),
                sg.Button(f"{SAVE_ICON} Save", key=SAVE_EVENT),
                sg.Text(" ", size=SPACER_SIZE),
                sg.Button(f"{SAVE_ICON} Save & Close", key=SAVE_CLOSE_EVENT),
            ],
        ]
        self._window = sg.Window("Edit Todo Item", layout=layout, finalize=True)
        self.todo_item = todo_item
        HandlerRegistry().register(self._window, self.handle_event)
        return self.window

    def save(self, values: dict[str, Any], close: bool = False):
        self.todo_item.title = values[TITLE_KEY]
        self.todo_item.category = values[CATEGORY_KEY]
        self.todo_item.description = values[DESCRIPTION_KEY]
        self.todo_item.notes = values[NOTES_KEY]
        self.todo_item.due_date = values[DUE_DATE_KEY]
        print(f'Saving "{self.todo_item.file_path}"')
        run(self.todo_service.save_todo(self.todo_item))
        if close:
            self.window.write_event_value(EXIT_EVENT, None)

    def delete(self):
        run(self.todo_service.delete_todo(self.todo_item))
        self.window.write_event_value(EXIT_EVENT, None)

    def handle_event(self, event: str, values: dict[str, Any]):
        if event in [sg.WIN_CLOSED, EXIT_EVENT]:
            HandlerRegistry().cancel(self.window)
            self.window.close()
            self._window = None
        elif event == SAVE_EVENT:
            self.window.start_thread(lambda: self.save(values))
        elif event == SAVE_CLOSE_EVENT:
            self.window.start_thread(lambda: self.save(values, close=True))
        elif event == DELETE_EVENT:
            self.window.start_thread(lambda: self.delete())


class TodoListGui:
    todo_service: TodoItemService = TodoItemService()
    todo_editor: TodoEditorGui | None = None
    _window: sg.Window | None = None

    @property
    def window(self) -> sg.Window:
        if self._window is None:
            self._window = self.create_window(self.todo_service.todo_items)
            HandlerRegistry().register(self._window, self.handle_event)
        return self._window

    def make_todo_row_item(self, todo_item: TodoItem) -> list:
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
                    key=(ROW_KEY, todo_item.id),
                    metadata=todo_item,
                )
            )
        ]
        return row

    def create_window(self, todo_items: list[TodoItem] | None = None) -> sg.Window:
        if todo_items is None:
            todo_items = self.todo_service.todo_items
        layout = [
            [sg.Text("Todo Items", font=DEFAULT_FONT_CONFIG)],
            [
                sg.Column(
                    [self.make_todo_row_item(todo_item) for todo_item in todo_items],
                    key=TODO_LIST_KEY,
                )
            ],
            [
                sg.Button(f"{NEW_ICON} New Todo", key=ADD_EVENT, tooltip="Create a new todo item"),
                sg.Button(f"{SAVE_ICON} Save", key=SAVE_EVENT, tooltip="Save your todo items"),
                sg.Button(EXIT_EVENT, k=EXIT_EVENT, tooltip="Close application"),
            ],
            [
                sg.Multiline(
                    size=DIAGNOSTICS_FIELD_SIZE,
                    k="-STDOUT-",
                    reroute_stdout=True,
                    write_only=True,
                    autoscroll=True,
                    auto_refresh=True,
                    reroute_cprint=True,
                )
            ],
        ]

        right_click_menu = [[""], [VERSION_EVENT, EXIT_EVENT]]

        window = sg.Window(
            "My Todo List",
            layout,
            right_click_menu=right_click_menu,
            use_default_focus=False,
            font=DEFAULT_FONT_CONFIG,
            metadata=1,
        )
        self._window = window
        return window

    def new_todo_item(self) -> None:
        print("Creating new todo item...")
        new_item = run(self.todo_service.new_todo(DEFAULT_TITLE_TEXT))
        self.window.extend_layout(
            self.window[TODO_LIST_KEY],
            [self.make_todo_row_item(new_item)],
        )
        print(f"Todo item #{new_item.id} was created")

    def save_todo_item(self, todo_item: TodoItem) -> None:
        print(f"Saving {todo_item.id}-{todo_item.title} to {todo_item.file_path}...")
        run(self.todo_service.save_todo(todo_item))
        print(f"{todo_item.id}-{todo_item.title} saved as {todo_item.file_path}")

    def save_todo_list(self) -> None:
        for todo_item in self.todo_service.todo_items:
            self.save_todo_item(todo_item)

    def handle_event(self, event: str, _: dict[str, Any]) -> None:
        if event == sg.WIN_CLOSED or event == EXIT_EVENT:
            HandlerRegistry().cancel(self.window)
            self.window.close()
            self._window = None
        elif event == ADD_EVENT:
            self.window.start_thread(lambda: self.new_todo_item())
        elif event == SAVE_EVENT:
            self.window.start_thread(lambda: self.save_todo_list())
        elif event == VERSION_EVENT:
            sg.popup_scrolled(
                __file__,
                sg.get_versions(),
                location=self.window.current_location(),
                keep_on_top=True,
                non_blocking=True,
            )
        elif event[0] == DELETE_EVENT:
            self.window[(ROW_KEY, event[1])].update(visible=False)  # type: ignore
        elif event[0] == EDIT_EVENT:
            id: int = int(event[1])
            todo_item = next(
                todo_item
                for todo_item in self.todo_service.todo_items
                if todo_item.id == id
            )
            if self.todo_editor is None:
                self.todo_editor = TodoEditorGui(todo_item)
            self.todo_editor.get_todo_editor(todo_item)
