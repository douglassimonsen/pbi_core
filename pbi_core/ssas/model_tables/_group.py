from typing import Any, Callable, Protocol, TypeVar


class idThing(Protocol):
    id: int


T = TypeVar("T", bound=idThing)


class RowNotFoundError(Exception):
    pass


class Group(list[T]):
    def find(self, match_val: int | dict[str, Any] | Callable[[T], bool]) -> T:
        """
        Finds a matching SSAS record from the group using the following rules:
        1. If match_val is an int, it finds a record with a matching `id`
        2. If match_val is a dictionary, it uses the keys as field names and values as field values. It returns the first record to match all items
        3. If match_val is a function, it returns the first record to return true when passed to the function
        """
        if isinstance(match_val, int):
            for val in self:
                if val.id == match_val:
                    return val
        elif isinstance(match_val, dict):
            for val in self:
                if all(getattr(val, field_name) == field_value for field_name, field_value in match_val.items()):
                    return val

        else:
            for val in self:
                if match_val(val) is True:
                    return val
        raise RowNotFoundError

    def find_all(self, match_val: int | dict[str, Any] | Callable[[T], bool]) -> list[T]:
        ret: list[T] = []
        if isinstance(match_val, int):
            for val in self:
                if val.id == match_val:
                    ret.append(val)
        elif isinstance(match_val, dict):
            for val in self:
                if all(getattr(val, field_name) == field_value for field_name, field_value in match_val.items()):
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
