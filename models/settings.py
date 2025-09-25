from dataclasses import dataclass, field
from pathlib import Path
from typing import Self
from mixins.dataclass_json import CustomDataClassJsonMixin

SETTINGS_FILENAME = "todo-settings.json"

@dataclass
class AppSettings(CustomDataClassJsonMixin):
    default_directory: Path = field(
        metadata={
            "dataclasses_json": {
                "encoder": Path.as_uri,
                "decoder": Path.from_uri
            }
        },
        default=Path.cwd(),
    )
    settings_file_path: Path = field(
        metadata={
            "dataclasses_json": {
                "encoder": Path.as_uri,
                "decoder": Path.from_uri
            }
        },
        default=Path.cwd() / SETTINGS_FILENAME,
    )
    async def reload(self)->Self:
        return await self.read_file(self.settings_file_path)
