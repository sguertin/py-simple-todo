from models.todo import TodoItem
import FreeSimpleGUI as sg

ADD_EVENT = '-ADD-'
REFRESH_EVENT = '-REFRESH-'
EXIT_EVENT = 'Exit'
TODO_LIST_ID = '-TODO LIST-'
DEFAULT_TEXT = 'Get Something Done!'

SMALL_COLUMN_SIZE = (4, 1)
MEDIUM_COLUMN_SIZE = (25, 1)
LARGE_COLUMN_SIZE = (55, 1)
DEFAULT_FONT_SIZE = '_ 15'
COLUMN_FONT_SIZE = '_ 12'
THEME = 'DarkGrey14'
    
def make_todo_item(todo_item: TodoItem)->list:
    row =  [sg.pin(sg.Col([[
        sg.Text(f'{todo_item.id}.', size=SMALL_COLUMN_SIZE, metadata=todo_item), 
        sg.Checkbox('', key=f'-CHECK-{todo_item.id}-', size=SMALL_COLUMN_SIZE, metadata=todo_item, tooltip='Mark Todo Item as Complete/Incomplete'), 
        sg.Input(todo_item.title, k=f'-TITLE-{todo_item.id}', size=MEDIUM_COLUMN_SIZE, metadata=todo_item, tooltip='Title of Todo Item'), 
        sg.Input(todo_item.description,  k=f'-DESCRIPTION-{todo_item.id}-', size=LARGE_COLUMN_SIZE, metadata=todo_item, tooltip='Description of Todo Item'), 
        sg.Button('X', border_width=0, button_color=(sg.theme_text_color(), sg.theme_background_color()), k=('-DEL-', todo_item.id), tooltip='Delete this item', size=SMALL_COLUMN_SIZE, metadata=todo_item)
    ]], k=('-ROW-', todo_item.id)))] 
    return row


def make_window()->sg.Window:

    layout = [  
                [sg.Text('Todo Items', font='_ 15')],
                [sg.Column([make_todo_item(TodoItem(1, DEFAULT_TEXT))], k=TODO_LIST_ID)],
                [
                    sg.Button('New Todo', key=ADD_EVENT, tooltip='Create a new todo item', button_color=(sg.theme_text_color(), sg.theme_background_color())),
                    sg.Button('Exit', k=EXIT_EVENT, tooltip='Close application', button_color=(sg.theme_text_color(), sg.theme_background_color())),                    
                ]
            ]

    right_click_menu = [[''], ['Version', EXIT_EVENT]]

    window = sg.Window('My Todo List', layout,  right_click_menu=right_click_menu, use_default_focus=False, font='_ 15', metadata=1)

    return window


def main():
    sg.theme(THEME)
    window = make_window()
    while True:
        event, values = window.read()     # type: ignore # wake every hour
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == ADD_EVENT:
            window.metadata += 1
            window.extend_layout(window[TODO_LIST_ID], [make_todo_item(TodoItem(window.metadata, DEFAULT_TEXT))])
        elif event == 'Version':
            sg.popup_scrolled(__file__, sg.get_versions(), location=window.current_location(), keep_on_top=True, non_blocking=True)
        elif event[0] == '-DEL-':
                window[('-ROW-', event[1])].update(visible=False) # type: ignore
    window.close()


if __name__ == '__main__':
    main()
