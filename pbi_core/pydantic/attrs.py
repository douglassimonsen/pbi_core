import json
from typing import TYPE_CHECKING, Self, TypeVar

from attrs import define as _define

if TYPE_CHECKING:
    from collections.abc import Callable

    from attrs import _C

T = TypeVar("T")


def define(
    *,
    kw_only: bool = True,
    eq: bool = True,
    hash: bool = True,  # noqa: A002
    slots: bool = False,
    init: bool = True,
) -> "Callable[[_C], _C]":
    return _define(slots=slots, kw_only=kw_only, hash=hash, eq=eq, init=init)


class BaseValidation:
    @classmethod
    def model_validate(cls, data: dict) -> Self:
        from pbi_core.pydantic.cattrs import converter  # noqa: PLC0415

        return converter.structure(data, cls)

    def model_dump(self) -> dict:
        from pbi_core.pydantic.cattrs import converter  # noqa: PLC0415

        return converter.unstructure(self)

    def model_dump_json(self, indent: int = 4) -> str:
        return json.dumps(self.model_dump(), indent=indent)
