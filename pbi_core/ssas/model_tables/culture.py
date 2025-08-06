import datetime
from typing import TYPE_CHECKING

from ...lineage import LineageNode
from ..server.tabular_model import SsasRenameTable

if TYPE_CHECKING:
    from .linguistic_metadata import LinguisticMetadata
    from .model import Model


class Culture(SsasRenameTable):
    linguistic_metadata_id: int
    model_id: int
    name: str

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def linguistic_metdata(self) -> "LinguisticMetadata":
        return self.tabular_model.linguistic_metadata.find({"id": self.linguistic_metadata_id})

    def model(self) -> "Model":
        return self.tabular_model.model

    def get_lineage(self, children: bool = False, parents: bool = True) -> LineageNode:
        return LineageNode(self, [self.linguistic_metdata().get_lineage(), self.model().get_lineage()])
