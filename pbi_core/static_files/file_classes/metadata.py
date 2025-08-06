from typing import Any

from ._base import BaseFileModel

base_val = bool | int | str


class Metadata(BaseFileModel):
    Version: int
    AutoCreatedRelationships: list[Any] = []
    CreatedFrom: str
    CreatedFromRelease: str
    FileDescription: str | None = None
