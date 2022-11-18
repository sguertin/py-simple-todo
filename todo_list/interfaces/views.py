from abc import ABCMeta, abstractmethod

from typing import Any

from todo_list.models.events import Events


class IView(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: "IView"):
        return (hasattr(subclass, "run") and callable(subclass.run)) or NotImplemented

    @abstractmethod
    def run(self) -> tuple[Events, dict[str, Any]]:
        raise NotImplementedError(self.run)
