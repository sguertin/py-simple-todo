from asyncio import run
from pathlib import Path
from threading import Lock

import aiofiles

from models.settings import AppSettings, SETTINGS_FILENAME

STARTUP_DIR = Path.cwd()

class SettingsProvider:
    _settings: AppSettings
    _lock = Lock()
    _file_lock = Lock()
    
    @property    
    def settings(self)->AppSettings:
        return self._settings
    
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
        with self._file_lock:
            async with aiofiles.open(self._settings.file_path, 'r+') as f:
                self._settings = AppSettings.from_json(await f.read())
        
    async def save_settings(self, settings: AppSettings) -> None:
        with self._file_lock:
            async with aiofiles.open(settings.file_path, 'w+') as f:
                await f.write(settings.to_json())

run(SettingsProvider._new(STARTUP_DIR))