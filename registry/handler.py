from types import MethodType
from typing import Any
from threading import Lock

import FreeSimpleGUI as sg

class HandlerRegistry:
    _lock = Lock()
    _handlers: dict[sg.Window, MethodType] = {}
    
    def __new__(cls):
        with cls._lock:
            if not hasattr(cls, "instance"):        
                cls.instance = super(HandlerRegistry, cls).__new__(cls)
        return cls.instance
    
    def register(self, window: sg.Window, handler: MethodType)->None:
        if window not in self._handlers:
            self._handlers[window] = handler

    def cancel(self, window: sg.Window)->None:
        if window in self._handlers:
            del self._handlers[window]
    
    def handle_events(self, window: sg.Window, event: str, values: dict[str, Any]):
        if window is None:
            return        
        if window in self._handlers:
            self._handlers[window](event, values)
        else:
            raise KeyError("Could not find handler for window")