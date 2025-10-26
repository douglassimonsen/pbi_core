from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from .main import LayoutNode

LAYOUT_ENCODING = "utf-16-le"


T = TypeVar("T", bound="LayoutNode")


def _gen_find_filter_callable(attributes: dict[str, Any] | Callable[[T], bool] | None) -> Callable[[T], bool]:
    if attributes is None:
        attribute_lambda: Callable[[T], bool] = lambda _: True  # noqa: E731
    elif isinstance(attributes, dict):
        attribute_lambda = lambda x: all(  # noqa: E731
            getattr(x, field_name) == field_value for field_name, field_value in attributes.items()
        )
    else:
        attribute_lambda = attributes
    return attribute_lambda


class FindMixin:
    def find_all(
        self,
        cls_type: type[T] | tuple[type[T], ...],
        attributes: dict[str, Any] | Callable[[T], bool] | None = None,
    ) -> list["T"]:
        ret: list[T] = []
        from .main import LayoutNode  # noqa: PLC0415

        assert isinstance(self, LayoutNode)

        attribute_lambda = _gen_find_filter_callable(attributes)
        if isinstance(self, cls_type) and attribute_lambda(self):
            ret.append(self)
        for child in self._children():
            ret.extend(child.find_all(cls_type, attribute_lambda))
        return ret

    def find(self, cls_type: type[T], attributes: dict[str, Any] | Callable[[T], bool] | None = None) -> "T":
        from .main import LayoutNode  # noqa: PLC0415

        assert isinstance(self, LayoutNode)

        attribute_lambda = _gen_find_filter_callable(attributes)
        if isinstance(self, cls_type) and attribute_lambda(self):
            return self
        for child in self._children():
            try:
                return child.find(cls_type, attribute_lambda)
            except ValueError:
                pass
        msg = f"Object not found: {cls_type}"
        raise ValueError(msg)
