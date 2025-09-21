import json
from types import UnionType
from typing import Any, TypeVar, Union, get_args, get_origin
from uuid import UUID

import cattrs

T = TypeVar("T")


def _is_union(tp: Any) -> bool:
    o = get_origin(tp)
    return o is Union or o is UnionType  # supports PEP 604: A | B


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


converter = cattrs.Converter()
converter.register_structure_hook_func(_is_union, _structure_union)
converter.register_structure_hook_func(_is_json, _structure_json)
converter.register_structure_hook(UUID, lambda obj, _: UUID(obj))
