from constants.events import DEFAULT_EVENT
from gui.todo import TodoListGui
from rich import print
import FreeSimpleGUI as sg

from models.settings import AppSettings
from providers.settings import SettingsProvider
from registry.handler import HandlerRegistry
handler_registry: HandlerRegistry = HandlerRegistry()
settings: AppSettings = SettingsProvider().settings
todo_list_gui: TodoListGui = TodoListGui()
windows = []
def main():
    sg.theme(settings.theme)
    windows.append(todo_list_gui.create_window())
    while any(windows):
        window, event, values = sg.read_all_windows()
        if event == sg.TIMEOUT_EVENT:
            continue
        if window is None:
            print('exiting because no windows are left')
            break
        if event is None:
            event = DEFAULT_EVENT 
        if values is None:
            values = {}
        print(f"Window('{window.Title}')",event, values)
        handler_registry.handle_events(window, event, values)

if __name__ == '__main__':
    main()
