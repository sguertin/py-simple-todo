import FreeSimpleGUI as sg
from models.todo import TodoItem

CALENDAR_ICON = "璘"

def make_todo_editor_layout(todo_item: TodoItem)->sg.Window:
    due_date = (None, None, None)
    due_date_text = ''
    if todo_item.due_date is not None:
        due_date = (todo_item.due_date.month, todo_item.due_date.day, todo_item.due_date.year)
        due_date_text = todo_item.due_date.strftime("%d/%m/%Y")
    layout = [
            [sg.Text('Id:', size=(8,1)), sg.Text(str(todo_item.id), size=(8,1))],
            [sg.Text('Title:', size=(8,1)), sg.Input(default_text=todo_item.title, key=('-Title-', todo_item), do_not_clear=False, size=(31,1))],
            [sg.Text('Due Date:', size=(8,1)),sg.Input(default_text=due_date_text, key=('-DueDate-', todo_item), do_not_clear=False, size=(28,1)), sg.CalendarButton(CALENDAR_ICON, default_date_m_d_y=due_date)],
            [sg.Text('Category:', size=(8,1)), sg.Input(default_text=todo_item.category, key=('-Category-', todo_item), do_not_clear=False, size=(31,1))],
            [sg.Text('Description', size=(8,1))],
            [sg.Text(' ', size=(8,1)), sg.Multiline(size=(31,12), key='-Description-', do_not_clear=False)],
            [sg.Text('Notes', size=(8,1))],
            [sg.Text(' ', size=(8,1)), sg.Multiline(size=(31,17), key='-Notes-', do_not_clear=False)],
            [sg.Text(' '*77), sg.Button('Save', key=('-Save-', todo_item))]
        ]
    return sg.Window('Edit Todo Item', layout=layout, finalize=True)


    
# window = sg.Window('Ticket Reservation', layout)

# while True:             # Event Loop
#     event, values = window.read() # type: ignore
#     if event in (None, 'Exit'):
#         break
#     sg.popup('Values entered', values['-NAME-'], 'Male' if values['-MALE-'] else 'Female', values['-COMMENTS-'])
#     window['-NAME-'].set_focus() # type: ignore
# window.close()