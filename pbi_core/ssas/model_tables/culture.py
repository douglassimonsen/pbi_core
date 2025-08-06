import datetime
from typing import TYPE_CHECKING

from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands

if TYPE_CHECKING:
    from .linguistic_metadata import LinguisticMetadata
    from .model import Model


class Culture(SsasTable):
    _commands: SsasRenameCommands
    linguistic_metadata_id: int
    model_id: int
    name: str

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def linguistic_metdata(self) -> "LinguisticMetadata":
        return self.tabular_model.linguistic_metadata.find({"id": self.linguistic_metadata_id})

    def model(self) -> "Model":
        return self.tabular_model.model
