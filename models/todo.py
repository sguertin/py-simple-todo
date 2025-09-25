from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import aiofiles

from mixins.dataclass_json import CustomDataClassJsonMixin

EMPTY = ""

@dataclass
class TodoItem(CustomDataClassJsonMixin):
    id: int
    title: str
    description: str = EMPTY
    category: str = EMPTY
    notes: str = EMPTY
    file_path: Optional[Path] = field(
        metadata={'dataclasses_json': {
            'encoder': str,
            'decoder': Path
        }}, default=None
    )
    done: bool = False
    due_date: Optional[datetime] = field(
        metadata={'dataclasses_json': {
            'encoder': datetime.isoformat,
            'decoder': datetime.fromisoformat
        }}, default=None
    )
    last_modified: datetime = field(
        metadata={'dataclasses_json': {
            'encoder': datetime.isoformat,
            'decoder': datetime.fromisoformat
        }}, default=datetime.now()
    )
    created: datetime = field(
        metadata={'dataclasses_json': {
            'encoder': datetime.isoformat,
            'decoder': datetime.fromisoformat
        }}, default=datetime.now()
    )
    
    async def write(self, file_path: Optional[Path] = None)->None:
        if file_path is not None:
            self.file_path = file_path
        if self.file_path is None:
            raise ValueError("Must specify a file_path!")
        async with aiofiles.open(self.file_path, 'w+') as f:
            await f.write(self.to_json())
    
    @classmethod
    async def read_file(cls, file_path: Path) -> 'TodoItem':
        async with aiofiles.open(file_path, 'r+') as f:
            return cls.from_json(await f.read())
