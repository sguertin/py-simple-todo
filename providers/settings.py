from asyncio import run
from pathlib import Path
from threading import Lock
from models.settings import AppSettings, SETTINGS_FILENAME

STARTUP_DIR = Path.cwd()

class SettingsProvider:
    _settings: AppSettings
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if not hasattr(cls, "instance"):        
                cls.instance = super(SettingsProvider, cls).__new__(cls)
        return cls.instance    

    @classmethod
    async def _new(cls, working_directory: Path)->'SettingsProvider':
        settings = cls()
        await settings._init(working_directory)
        return settings
    
    async def _init(self, working_directory: Path = STARTUP_DIR):        
        settings_file_path = working_directory / SETTINGS_FILENAME
        self._settings = AppSettings(default_directory=working_directory, settings_file_path=settings_file_path)
        if settings_file_path.exists():
            await self.reload()
        else:            
            if not working_directory.exists():
                working_directory.mkdir()
            await self.save_settings(self._settings)
        
    async def reload(self)->None:
        await self._settings.reload()
        
    def get_settings(self)->AppSettings:
        return self._settings
    
    async def save_settings(self, settings: AppSettings) -> None:
        with self._lock:
            self._settings = settings        
            await settings.write()

run(SettingsProvider._new(STARTUP_DIR))