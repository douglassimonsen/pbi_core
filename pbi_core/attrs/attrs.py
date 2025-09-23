import json
from typing import TYPE_CHECKING, Any, Self, TypeVar, dataclass_transform

from attr._make import Attribute
from attrs import define as _define
from attrs import field

if TYPE_CHECKING:
    from collections.abc import Callable

    from attrs import _C


T = TypeVar("T")


@dataclass_transform(kw_only_default=True)
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
    _original_data: Any = field(init=False, repr=False, hash=False, eq=False)
    __attrs_attrs__: tuple[Attribute, ...]

    @classmethod
    def model_validate(cls, data: dict) -> Self:
        from .cattrs import converter  # noqa: PLC0415

        return converter.structure(data, cls)

    @classmethod
    def model_validate_json(cls, data: str) -> Self:
        return cls.model_validate(json.loads(data))

    def model_dump(self) -> dict:
        from .cattrs import converter  # noqa: PLC0415

        return converter.unstructure(self)

    def model_dump_json(self, indent: int = 4) -> str:
        return json.dumps(self.model_dump(), indent=indent)
