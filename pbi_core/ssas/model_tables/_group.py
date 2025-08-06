from typing import Callable, Protocol, Sequence, TypeVar


class idThing(Protocol):
    id: int


T = TypeVar("T", bound=idThing)


class Group(Sequence[T]):
    def get(self, match_val: int | Callable[[T], bool]) -> T:
        if isinstance(match_val, int):
            for val in self:
                if val.id == match_val:
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
