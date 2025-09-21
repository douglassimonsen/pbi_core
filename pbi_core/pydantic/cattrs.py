import json
from collections.abc import Callable
from types import UnionType
from typing import Any, TypeVar, Union, get_args, get_origin
from uuid import UUID

import cattrs

T = TypeVar("T")
# cursed, but I don't know how else to identify annotated unions


def _is_union(tp: Any) -> bool:
    o = get_origin(tp)
    if o is Union:  # typing.Union[...]
        return True
    if o is UnionType:  # PEP 604 union (A | B)  # noqa: SIM103
        return True
    return False


def _structure_union(val: Any, tp: Any) -> Any:
    args = get_args(tp)

    # Optional fast-path: Union[T, NoneType]
    non_none = tuple(a for a in args if a is not type(None))
    if len(non_none) + 1 == len(args) and len(args) >= 2:  # noqa: PLR2004
        if val is None:
            return None
        last_err = None
        for a in non_none:
            try:
                return converter.structure(val, a)
            except Exception as e:  # be permissive; keep trying  # noqa: BLE001
                last_err = e
        raise last_err or ValueError(val, tp)

    # General Union: try each member type in order
    last_err = None
    for a in args:
        try:
            return converter.structure(val, a)
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise last_err or ValueError(val, tp)


def _is_json(tp: Any) -> bool:
    return bool(hasattr(tp, "__metadata__") and tp.__metadata__[0].__class__.__name__ == "Json")


def _structure_json(val: Any, tp: Any) -> Any:
    if not isinstance(val, str):
        msg = f"Expected JSON string, got {type(val)}"
        raise TypeError(msg)
    unwrapped = json.loads(val)
    return converter.structure(unwrapped, tp.__args__[0])


def unstruct_json(val: Any) -> str:
    unwrapped = converter.unstructure(val)
    return json.dumps(unwrapped)


def tagged_union_checker(tp: UnionType, tp_name: str) -> Callable[[Any], bool]:
    def inner(v: Any) -> bool:
        if isinstance(v, UnionType):
            return v is tp
        if isinstance(v, str):
            return v == tp_name
        return False

    return inner


def struct_uuid(obj: Any, _: Any = None) -> UUID:
    if isinstance(obj, UUID):
        return obj
    if isinstance(obj, str):
        return UUID(obj)
    raise TypeError(f"Cannot convert {obj!r} to UUID")


def unstruct_uuid(obj: UUID) -> str:
    return str(obj)


def unstruct_union(obj: Any) -> Any:
    return converter.unstructure(obj)


converter = cattrs.GenConverter(forbid_extra_keys=True, omit_if_default=True)

converter.register_structure_hook_func(_is_union, _structure_union)
converter.register_unstructure_hook_func(_is_union, unstruct_union)

converter.register_structure_hook_func(_is_json, _structure_json)
converter.register_unstructure_hook_func(_is_json, unstruct_json)


converter.register_structure_hook(UUID, struct_uuid)
converter.register_unstructure_hook(UUID, unstruct_uuid)
