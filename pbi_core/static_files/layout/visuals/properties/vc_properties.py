from pydantic import Field

from pbi_core.static_files.layout._base_node import LayoutNode

from .base import Expression


class Background(LayoutNode):
    class _BackgroundProperties(LayoutNode):
        color: Expression | None = None
        show: Expression | None = None
        transparency: Expression | None = None

    properties: _BackgroundProperties = Field(default_factory=_BackgroundProperties)


class Border(LayoutNode):
    class _BorderProperties(LayoutNode):
        background: Expression | None = None
        color: Expression | None = None
        radius: Expression | None = None
        show: Expression | None = None

    properties: _BorderProperties = Field(default_factory=_BorderProperties)


class DropShadow(LayoutNode):
    class _DropShadowProperties(LayoutNode):
        angle: Expression | None = None
        color: Expression | None = None
        position: Expression | None = None
        preset: Expression | None = None
        shadowBlur: Expression | None = None
        shadowDistance: Expression | None = None
        shadowSpread: Expression | None = None
        show: Expression | None = None
        transparency: Expression | None = None

    properties: _DropShadowProperties


class General(LayoutNode):
    class _GeneralProperties(LayoutNode):
        altText: Expression | None = None
        keepLayerOrder: Expression | None = None

    properties: _GeneralProperties = Field(default_factory=_GeneralProperties)


class LockAspect(LayoutNode):
    class _LockAspectProperties(LayoutNode):
        show: Expression | None = None

    properties: _LockAspectProperties


class StylePreset(LayoutNode):
    class _StylePresetProperties(LayoutNode):
        name: Expression | None = None

    properties: _StylePresetProperties = Field(default_factory=_StylePresetProperties)


class Title(LayoutNode):
    class _TitleProperties(LayoutNode):
        alignment: Expression | None = None
        background: Expression | None = None
        fontColor: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        heading: Expression | None = None
        show: Expression | None = None
        text: Expression | None = None
        titleWrap: Expression | None = None

    properties: _TitleProperties = Field(default_factory=_TitleProperties)


class VisualHeader(LayoutNode):
    class _VisualHeaderProperties(LayoutNode):
        background: Expression | None = None
        border: Expression | None = None
        foreground: Expression | None = None
        show: Expression | None = None
        showDrillDownExpandButton: Expression | None = None
        showDrillDownLevelButton: Expression | None = None
        showDrillRoleSelector: Expression | None = None
        showDrillToggleButton: Expression | None = None
        showDrillUpButton: Expression | None = None
        showFilterRestatementButton: Expression | None = None
        showFocusModeButton: Expression | None = None
        showOptionsMenu: Expression | None = None
        showPinButton: Expression | None = None
        showSeeDataLayoutToggleButton: Expression | None = None
        showSmartNarrativeButton: Expression | None = None
        showTooltipButton: Expression | None = None
        showVisualErrorButton: Expression | None = None
        showVisualInformationButton: Expression | None = None
        showVisualWarningButton: Expression | None = None
        transparency: Expression | None = None

    properties: _VisualHeaderProperties = Field(default_factory=_VisualHeaderProperties)


class VisualHeaderTooltip(LayoutNode):
    class _VisualHeaderTooltipProperties(LayoutNode):
        background: Expression | None = None
        section: Expression | None = None
        text: Expression | None = None
        themedBackground: Expression | None = None
        themedTitleFontColor: Expression | None = None
        titleFontColor: Expression | None = None
        transparency: Expression | None = None
        type: Expression | None = None

    properties: _VisualHeaderTooltipProperties


class VisualLink(LayoutNode):
    class _VisualLinkProperties(LayoutNode):
        bookmark: Expression | None = None
        disabledTooltip: Expression | None = None
        drillthroughSection: Expression | None = None
        enabledTooltip: Expression | None = None
        navigationSection: Expression | None = None
        show: Expression | None = None
        tooltip: Expression | None = None
        type: Expression | None = None
        webUrl: Expression | None = None

    properties: _VisualLinkProperties = Field(default_factory=_VisualLinkProperties)


class VisualTooltip(LayoutNode):
    class _VisualTooltipProperties(LayoutNode):
        background: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        section: Expression | None = None
        show: Expression | None = None
        titleFontColor: Expression | None = None
        type: Expression | None = None
        valueFontColor: Expression | None = None

    properties: _VisualTooltipProperties = Field(default_factory=_VisualTooltipProperties)


class VCProperties(LayoutNode):
    background: list[Background] | None = None
    border: list[Border] | None = None
    dropShadow: list[DropShadow] | None = None
    general: list[General] | None = None
    lockAspect: list[LockAspect] | None = None
    stylePreset: list[StylePreset] | None = None
    title: list[Title] | None = None
    visualHeader: list[VisualHeader] | None = None
    visualHeaderTooltip: list[VisualHeaderTooltip] | None = None
    visualLink: list[VisualLink] | None = None
    visualTooltip: list[VisualTooltip] | None = None
