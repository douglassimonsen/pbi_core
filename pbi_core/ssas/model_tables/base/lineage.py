from typing import TYPE_CHECKING, Literal

from structlog import get_logger

from pbi_core.attrs import define
from pbi_core.lineage import LineageNode

if TYPE_CHECKING:
    from .ssas_tables import SsasTable
logger = get_logger()


@define()
class LineageMixin:
    def parents(self, *, recursive: bool = True) -> frozenset["SsasTable"]:  # noqa: ARG002, PLR6301
        return frozenset()

    @staticmethod
    def _recurse_parents(parents: frozenset["SsasTable"]) -> frozenset["SsasTable"]:
        ret = set(parents)
        for p in parents:
            ret.update(p.parents(recursive=True))
        return frozenset(ret)

    def children(self, *, recursive: bool = True) -> frozenset["SsasTable"]:  # noqa: ARG002, PLR6301
        return frozenset()

    @staticmethod
    def _recurse_children(children: frozenset["SsasTable"]) -> frozenset["SsasTable"]:
        ret = set(children)
        for c in children:
            ret.update(c.children(recursive=True))
        return frozenset(ret)

    def get_lineage(self, lineage_type: Literal["children", "parents"]) -> LineageNode:
        """Creates a lineage node tracking the data parents/children of a record."""
        ancestors = self.children(recursive=False) if lineage_type == "children" else self.parents(recursive=False)
        relatives = [a.get_lineage(lineage_type) for a in ancestors]
        return LineageNode(self, lineage_type, relatives)
