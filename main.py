from models.todo import TodoItem

from rich import print
import FreeSimpleGUI as sg

ADD_EVENT = '-ADD-'
SAVE_EVENT = '-SAVE-'
EDIT_EVENT = '-EDIT-'
DELETE_EVENT = '-DEL-'
EXIT_EVENT = 'Exit'
VERSION_EVENT = 'Version'

TODO_LIST_ID = '-TODO LIST-'
ROW_ID = '-ROW-'

DEFAULT_TEXT = 'Get Something Done!'

SMALL_COLUMN_SIZE = (4, 1)
MEDIUM_COLUMN_SIZE = (25, 1)
LARGE_COLUMN_SIZE = (55, 1)
DEFAULT_FONT_SIZE = 'Delugia 15'
COLUMN_FONT_SIZE = 'Delugia 12'
THEME = 'DarkGrey14'
SAVE_ICON = ''
EDIT_ICON = ''
DELETE_ICON = ''
def make_todo_item(todo_item: TodoItem)->list:
    row =  [sg.pin(sg.Column([[
        sg.Text(f'{todo_item.id}.', size=SMALL_COLUMN_SIZE), 
        sg.Checkbox('', key=f'-CHECK-{todo_item.id}-', size=SMALL_COLUMN_SIZE, tooltip='Mark Todo Item as Complete/Incomplete'), 
        sg.Input(todo_item.title, k=f'-TITLE-{todo_item.id}', size=MEDIUM_COLUMN_SIZE, tooltip='Title of Todo Item'),
        sg.Button(EDIT_ICON, border_width=0, k=(EDIT_EVENT, todo_item.id), tooltip='Edit this todo item', size=SMALL_COLUMN_SIZE, metadata=todo_item), 
        sg.Button(DELETE_ICON, border_width=0, k=(DELETE_EVENT, todo_item.id), tooltip='Delete this todo item', size=SMALL_COLUMN_SIZE, metadata=todo_item)
    ]], key=(ROW_ID, todo_item.id), metadata=todo_item))] 
    return row


def make_window()->sg.Window:

    layout = [  
                [sg.Text('Todo Items', font=DEFAULT_FONT_SIZE)],
                [sg.Column([make_todo_item(TodoItem(1, DEFAULT_TEXT))], key=TODO_LIST_ID)],
                [
                    sg.Button('New Todo', key=ADD_EVENT, tooltip='Create a new todo item'),
                    sg.Button('', key=SAVE_EVENT, tooltip='NOT IMPLEMENTED'),
                    sg.Button(EXIT_EVENT, k=EXIT_EVENT, tooltip='Close application'),                    
                ]
            ]

    right_click_menu = [[''], ['Version', EXIT_EVENT]]

    window = sg.Window('My Todo List', layout,  right_click_menu=right_click_menu, use_default_focus=False, font=DEFAULT_FONT_SIZE, metadata=1)

    return window


def main():
    sg.theme(THEME)
    window = make_window()
    while True:
        event, values = window.read()     # type: ignore # wake every hour
        print(event, values)
        if event == sg.WIN_CLOSED or event == EXIT_EVENT:
            break
        if event == ADD_EVENT:
            window.metadata += 1
            window.extend_layout(window[TODO_LIST_ID], [make_todo_item(TodoItem(window.metadata, DEFAULT_TEXT))])
        elif event == VERSION_EVENT:
            sg.popup_scrolled(__file__, sg.get_versions(), location=window.current_location(), keep_on_top=True, non_blocking=True)
        elif event[0] == DELETE_EVENT:
                window[(ROW_ID, event[1])].update(visible=False) # type: ignore
    window.close()


if __name__ == '__main__':
    main()
