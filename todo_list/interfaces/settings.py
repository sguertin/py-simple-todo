from abc import ABCMeta, abstractmethod
from todo_list.models.settings import Settings


class ISettingsProvider(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "load") and callable(subclass.load))
            and (hasattr(subclass, "save") and callable(subclass.save))
            or NotImplemented
        )

    @abstractmethod
    def load(self) -> Settings:
        """Loads settings

        Returns:
            Settings: The retrieved settings
        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, settings: Settings) -> None:
        """Saves the provided settings

        Args:
            settings (Settings): The settings to be saved

        """
        raise NotImplementedError()
