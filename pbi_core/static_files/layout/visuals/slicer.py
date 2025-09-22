from attrs import field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.filters import Filter
from pbi_core.static_files.layout.selector import SelectorData

from .base import BaseVisual
from .properties.base import Expression


class SyncGroup(LayoutNode):
    groupName: str
    fieldChanges: bool
    filterChanges: bool = True


class CachedFilterDisplayItems(LayoutNode):
    id: SelectorData
    displayName: str


class DataProperties(LayoutNode):
    class _DataPropertiesHelper(LayoutNode):
        endDate: Expression | None = None
        isInvertedSelectionMode: Expression | None = None
        mode: Expression | None = None
        numericEnd: Expression | None = None
        numericStart: Expression | None = None
        startDate: Expression | None = None

    properties: _DataPropertiesHelper = field(factory=_DataPropertiesHelper)


class DateProperties(LayoutNode):
    class _DatePropertiesHelper(LayoutNode):
        background: Expression | None = None
        fontColor: Expression | None = None
        fontFamily: Expression | None = None
        textSize: Expression | None = None

    properties: _DatePropertiesHelper = field(factory=_DatePropertiesHelper)


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        filter: Filter | None = None
        responsive: Expression | None = None
        selfFilterEnabled: Expression | None = None
        selfFilter: Filter | None = None
        orientation: Expression | None = None
        outlineColor: Expression | None = None
        outlineWeight: Expression | None = None

    properties: _GeneralPropertiesHelper = field(factory=_GeneralPropertiesHelper)


class HeaderProperties(LayoutNode):
    class _HeaderPropertiesHelper(LayoutNode):
        background: Expression | None = None
        fontColor: Expression | None = None
        fontFamily: Expression | None = None
        outlineStyle: Expression | None = None
        show: Expression | None = None
        showRestatement: Expression | None = None
        text: Expression | None = None
        textSize: Expression | None = None
        underline: Expression | None = None

    properties: _HeaderPropertiesHelper = field(factory=_HeaderPropertiesHelper)


class NumericInputStyleProperties(LayoutNode):
    class _NumericInputStylePropertiesHelper(LayoutNode):
        background: Expression | None = None
        fontColor: Expression | None = None
        fontFamily: Expression | None = None
        textSize: Expression | None = None

    properties: _NumericInputStylePropertiesHelper = field(factory=_NumericInputStylePropertiesHelper)


class ItemProperties(LayoutNode):
    class _ItemPropertiesHelper(LayoutNode):
        background: Expression | None = None
        bold: Expression | None = None
        expandCollapseToggleType: Expression | None = None
        fontColor: Expression | None = None
        fontFamily: Expression | None = None
        outline: Expression | None = None
        outlineColor: Expression | None = None
        outlineStyle: Expression | None = None
        padding: Expression | None = None
        steppedLayoutIndentation: Expression | None = None
        textSize: Expression | None = None

    properties: _ItemPropertiesHelper = field(factory=_ItemPropertiesHelper)


class PendingChangeIconProperties(LayoutNode):
    class _PendingChangeIconPropertiesHelper(LayoutNode):
        color: Expression | None = None
        size: Expression | None = None
        tooltipLabel: Expression | None = None
        tooltipText: Expression | None = None
        transparency: Expression | None = None

    properties: _PendingChangeIconPropertiesHelper = field(factory=_PendingChangeIconPropertiesHelper)


class SelectionProperties(LayoutNode):
    class _SelectionPropertiesHelper(LayoutNode):
        selectAllCheckboxEnabled: Expression | None = None
        singleSelect: Expression | None = None
        strictSingleSelect: Expression | None = None

    properties: _SelectionPropertiesHelper = field(factory=_SelectionPropertiesHelper)


class SliderProperties(LayoutNode):
    class _SliderPropertiesHelper(LayoutNode):
        color: Expression | None = None
        show: Expression | None = None

    properties: _SliderPropertiesHelper = field(factory=_SliderPropertiesHelper)


class SlicerProperties(LayoutNode):
    date: list[DateProperties] = field(factory=lambda: [DateProperties()])
    data: list[DataProperties] = field(factory=lambda: [DataProperties()])
    general: list[GeneralProperties] = field(factory=lambda: [GeneralProperties()])
    header: list[HeaderProperties] = field(factory=lambda: [HeaderProperties()])
    items: list[ItemProperties] = field(factory=lambda: [ItemProperties()])
    numericInputStyle: list[NumericInputStyleProperties] = field(
        factory=lambda: [NumericInputStyleProperties()],
    )
    pendingChangesIcon: list[PendingChangeIconProperties] = field(
        factory=lambda: [PendingChangeIconProperties()],
    )
    selection: list[SelectionProperties] = field(factory=lambda: [SelectionProperties()])
    slider: list[SliderProperties] = field(factory=lambda: [SliderProperties()])


class Slicer(BaseVisual):
    visualType: str = "slicer"
    syncGroup: SyncGroup | None = None
    cachedFilterDisplayItems: list[CachedFilterDisplayItems] | None = None
    objects: SlicerProperties = field(factory=SlicerProperties)
