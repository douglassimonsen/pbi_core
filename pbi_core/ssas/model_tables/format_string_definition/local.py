import datetime
from typing import TYPE_CHECKING

from attrs import field, setters

from pbi_core.attrs import define

from .format_string_definition import FormatStringDefinition

if TYPE_CHECKING:
    from pbi_core.ssas.server import BaseTabularModel


# TODO: eventually only subclass from a MeasureDTO to emphasize that you
# shouldn't do most things with this object until it's created in SSAS
# We create a subclass rather than creating a .new method on Measure
# to expose the nice type hinting of the original object and to avoid
# bugs caused by trying to use a LocalFormatStringDefinition where a FormatStringDefinition is expected.
@define()
class LocalFormatStringDefinition(FormatStringDefinition):
    """Class for a Measure that does not yet exist in SSAS.

    Generally created for it's load command which instantiates the remote object in SSAS
    and then returns that remote object.
    """

    id: int = field(default=-1, on_setattr=setters.frozen)
    object_id: int = field(default=-1)  # pyright: ignore[reportIncompatibleVariableOverride]
    # The datatype will be inferred by SSAS on creation
    modified_time: datetime.datetime = field(  # pyright: ignore[reportGeneralTypeIssues]
        factory=lambda: datetime.datetime.now(datetime.UTC),
        on_setattr=setters.frozen,
    )

    def load(self, ssas: "BaseTabularModel") -> "FormatStringDefinition":
        remote = FormatStringDefinition._create_helper(self, ssas)
        ssas.format_string_definitions.append(remote)
        return remote
