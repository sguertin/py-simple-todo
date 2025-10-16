import asyncio
from abc import ABC, ABCMeta
import sys
import FreeSimpleGUI as sg

class AsyncMixin(ABC, metaclass=ABCMeta):
    window: sg.Window
    def run(self, command, end_event: str | None = None):
        try:
            self.window.start_thread(asyncio.run(command), end_event)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)