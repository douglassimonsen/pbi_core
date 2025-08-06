from typing import Any, Optional

from pydantic_extra_types.color import Color

from ._base import BaseFileModel

base_val = bool | int | str


class TextClass(BaseFileModel):
    fontSize: int
    fontFace: str
    color: Color


class TextClasses(BaseFileModel):
    callout: TextClass
    title: TextClass
    header: TextClass
    label: TextClass


class Theme(BaseFileModel):
    """
    A class mapping the fields of the Theme JSON documented `here <https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes#set-theme-colors>`
    """

    name: str
    dataColors: list[str] = []
    foreground: Optional[str] = None
    foregroundNeutralSecondary: Optional[Color] = None
    foregroundNeutralTertiary: Optional[Color] = None
    background: Optional[Color] = None
    backgroundLight: Optional[Color] = None
    backgroundNeutral: Optional[Color] = None
    tableAccent: Optional[Color] = None
    good: Optional[Color] = None
    neutral: Optional[Color] = None
    bad: Optional[Color] = None
    maximum: Optional[Color] = None
    center: Optional[Color] = None
    minimum: Optional[Color] = None
    null: Optional[Color] = None
    hyperlink: Optional[Color] = None
    visitedHyperlink: Optional[Color] = None

    textClasses: Optional[TextClasses] = None
    visualStyles: Any
