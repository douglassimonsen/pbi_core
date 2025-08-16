from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        fontSize: Expression | None = None
        funnelLabelStyle: Expression | None = None
        labelDisplayUnits: Expression | None = None
        percentageLabelPrecision: Expression | None = None
        show: Expression | None = None

    properties: _LabelsPropertiesHelper


class PercentBarLabelProperties(LayoutNode):
    class _PercentBarLabelPropertiesHelper(LayoutNode):
        color: Expression | None = None
        show: Expression | None = None

    properties: _PercentBarLabelPropertiesHelper


class CategoryAxisProperties(LayoutNode):
    class _CategoryAxisPropertiesHelper(LayoutNode):
        color: Expression | None = None
        show: Expression | None = None

    properties: _CategoryAxisPropertiesHelper


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        showAllDataPoints: Expression | None = None

    properties: _DataPointPropertiesHelper
    selector: Selector | None = None


class FunnelProperties(LayoutNode):
    categoryAxis: list[CategoryAxisProperties] | None = None
    dataPoint: list[DataPointProperties] | None = None
    labels: list[LabelsProperties] | None = None
    percentBarLabel: list[PercentBarLabelProperties] | None = None


class Funnel(BaseVisual):
    visualType: str = "funnel"
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
    drillFilterOtherVisuals: bool = True
    objects: FunnelProperties | None = None
