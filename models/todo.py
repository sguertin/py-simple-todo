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
    file_path: Path = field(
        metadata={'dataclasses_json': {
            'encoder': str,
            'decoder': Path
        }}, default=Path("1.todo")
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
    
    def __eq__(self, other: 'TodoItem')->bool:
        return self.id == other.id
