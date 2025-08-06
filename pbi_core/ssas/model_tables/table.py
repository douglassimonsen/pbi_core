import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import RefreshType, SsasRefreshTable

from .column import Column
from .measure import Measure
from .partition import Partition

if TYPE_CHECKING:
    from .model import Model


class Table(SsasRefreshTable):
    _refresh_type = RefreshType.DataOnly

    alternate_source_precedence: int
    data_category: str | None = None
    description: str | None = None
    exclude_from_model_refresh: bool
    is_hidden: bool
    is_private: bool
    lineage_tag: UUID
    model_id: int
    name: str
    show_as_variations_only: bool
    system_flags: int
    system_managed: bool | None = None
    table_storage_id: int | None = None

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def data(self, head: int = 100) -> list[dict[str, int | float | str]]:
        """Extracts records from the table in SSAS.

        Args:
            head (int): The number of records to return from the table.

        Returns:
            list[dict[str, int | float | str]]: A list of SSAS records in dictionary form.
                The keys are the field names and the values are the record values

        """
        return self.tabular_model.server.query_dax(
            f"EVALUATE TOPN({head}, ALL('{self.name}'))",
            db_name=self.tabular_model.db_name,
        )

    def partitions(self) -> list[Partition]:
        """Get associated dependent partitions.

        Returns:
            (list[Partition]): A list of the partitions containing data for this table

        """
        return self.tabular_model.partitions.find_all({"table_id": self.id})

    def columns(self) -> list[Column]:
        """Get associated dependent partitions.

        Returns:
            (list[Column]): A list of the columns in this table

        """
        return self.tabular_model.columns.find_all({"table_id": self.id})

    def table_measures(self) -> list[Measure]:
        """Get measures saved to this table.

        Returns:
            (list[Measure]): A list of measures saved to this table

        Note:
            These measures do not necessarily have calculations that depend on this table.
                For that use `table.measures()`

        """
        return self.tabular_model.measures.find_all({"table_id": self.id})

    def measures(self) -> list[Measure]:  # noqa: PLR6301
        """Get measures that logically depend on this table.

        Examples:
            .. code-block:: python
            :linenos:

            print(measure.expression)
            # sumx(example, [a])
            # Therefore, this measure would be returned by Table(name=example).measures()

        Returns:
            (list[Measure]): A list of measures that logically depend this table

        Note:
            These measures are not necessarily saved physically to this table. For that use `table.table_measures()`

        """
        return []

    def model(self) -> "Model":
        return self.tabular_model.model

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [col.get_lineage(lineage_type) for col in self.columns()]
                + [partition.get_lineage(lineage_type) for partition in self.partitions()]
                + [measure.get_lineage(lineage_type) for measure in self.measures()],
            )
        return LineageNode(self, lineage_type, [self.model().get_lineage(lineage_type)])

    def refresh(self) -> None:
        """Needs a model refresh to properly propogate the update."""
        super().refresh()
        self.model().refresh()
