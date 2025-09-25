from pathlib import Path
from typing import Self
from threading import Lock

import aiofiles
from dataclasses_json import DataClassJsonMixin, LetterCase, config


class CustomDataClassJsonMixin(DataClassJsonMixin):
    _lock = Lock()
    file_path: Path
    
    def __init__(self):
        self.dataclass_json_config = config(letter_case=LetterCase.CAMEL)
        
    async def write(self):
        with self._lock:
            async with aiofiles.open(self.file_path, 'w+') as f:
                await f.write(self.to_json())
            
    @classmethod
    async def read_file(cls, file_path: Path)->Self:
        async with aiofiles.open(file_path, 'r+') as f:
            return cls.from_json(await f.read())
