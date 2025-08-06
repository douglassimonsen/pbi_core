from typing import Any, Callable, Protocol, Sequence, TypeVar


class idThing(Protocol):
    id: int


T = TypeVar("T", bound=idThing)


class Group(Sequence[T]):
    def get(self, match_val: int | dict[str, Any] | Callable[[T], bool]) -> T:
        if isinstance(match_val, int):
            for val in self:
                if val.id == match_val:
                    return val
        elif isinstance(match_val, dict):
            for val in self:
                if all(getattr(self, field_name) == field_value for field_name, field_value in match_val.items()):
                    return val

        else:
            for val in self:
                if match_val(val) is True:
                    return val
        raise ValueError

    def find_all(self, match_val: int | dict[str, Any] | Callable[[T], bool]) -> list[T]:
        ret = []
        if isinstance(match_val, int):
            for val in self:
                if val.id == match_val:
                    ret.append(val)
        elif isinstance(match_val, dict):
            for val in self:
                if all(getattr(self, field_name) == field_value for field_name, field_value in match_val.items()):
                    ret.append(val)

        else:
            for val in self:
                if match_val(val) is True:
                    ret.append(val)
        return ret

    def sync_to_server(self) -> None:
        pass

    def sync_from_server(self) -> None:
        pass
