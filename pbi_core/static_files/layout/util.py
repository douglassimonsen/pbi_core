from collections.abc import Callable
from typing import TypeVar


class IdThing:
    def id(self) -> str:
        raise NotImplementedError


T = TypeVar("T", bound=IdThing)


class Group(list[T]):  # noqa: FURB189
    def get(self, match_val: str | Callable[[T], bool]) -> T:
        if isinstance(match_val, str):
            for val in self:
                if val.id() == match_val:
                    return val
        else:
            for val in self:
                if match_val(val) is True:
                    return val
        raise ValueError

    def sync_to_server(self) -> None:
        pass

    def sync_from_server(self) -> None:
        pass
