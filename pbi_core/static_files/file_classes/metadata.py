from typing import Any, Optional

from ._base import BaseFileModel

base_val = bool | int | str


class Metadata(BaseFileModel):
    Version: int
    AutoCreatedRelationships: list[Any] = []
    CreatedFrom: str
    CreatedFromRelease: str
    FileDescription: Optional[str] = None
