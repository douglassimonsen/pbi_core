from attrs import field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class CategoryAxisProperties(LayoutNode):
    class _CategoryAxisPropertiesHelper(LayoutNode):
        color: Expression | None = None
        show: Expression | None = None

    properties: _CategoryAxisPropertiesHelper = field(factory=_CategoryAxisPropertiesHelper)


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        showAllDataPoints: Expression | None = None

    properties: _DataPointPropertiesHelper = field(factory=_DataPointPropertiesHelper)
    selector: Selector | None = None


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        fontSize: Expression | None = None
        funnelLabelStyle: Expression | None = None
        labelDisplayUnits: Expression | None = None
        percentageLabelPrecision: Expression | None = None
        show: Expression | None = None

    properties: _LabelsPropertiesHelper = field(factory=_LabelsPropertiesHelper)


class PercentBarLabelProperties(LayoutNode):
    class _PercentBarLabelPropertiesHelper(LayoutNode):
        color: Expression | None = None
        show: Expression | None = None

    properties: _PercentBarLabelPropertiesHelper = field(factory=_PercentBarLabelPropertiesHelper)


class FunnelProperties(LayoutNode):
    categoryAxis: list[CategoryAxisProperties] = field(factory=lambda: [CategoryAxisProperties()])
    dataPoint: list[DataPointProperties] = field(factory=lambda: [DataPointProperties()])
    labels: list[LabelsProperties] = field(factory=lambda: [LabelsProperties()])
    percentBarLabel: list[PercentBarLabelProperties] = field(
        factory=lambda: [PercentBarLabelProperties()],
    )


class Funnel(BaseVisual):
    visualType: str = "funnel"
    drillFilterOtherVisuals: bool = True
    objects: FunnelProperties = field(factory=FunnelProperties, repr=False)
