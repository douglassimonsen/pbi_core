from typing import Any

from pydantic.color import Color

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
    foreground: str
    foregroundNeutralSecondary: Color
    foregroundNeutralTertiary: Color
    background: Color
    backgroundLight: Color
    backgroundNeutral: Color
    tableAccent: Color
    good: Color
    neutral: Color
    bad: Color
    maximum: Color
    center: Color
    minimum: Color
    null: Color
    hyperlink: Color
    visitedHyperlink: Color

    textClasses: TextClasses
    visualStyles: Any
