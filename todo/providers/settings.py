from todo.constants import SETTINGS_FILE
from todo.decorators import fire_and_forget
from todo.interfaces.settings import ISettingsProvider
from todo.models.settings import Settings


class MockSettingsProvider(ISettingsProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    def load(self) -> Settings:
        return self.settings

    def save(self, settings: Settings):
        self.settings = settings


class SettingsProvider(ISettingsProvider):
    def load(self) -> Settings:
        with open(SETTINGS_FILE, "r") as f:
            return Settings.from_json(f.read())

    @fire_and_forget
    def save(self, settings: Settings) -> None:
        with open(SETTINGS_FILE, "w+") as f:
            f.write(settings.to_json())
