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

