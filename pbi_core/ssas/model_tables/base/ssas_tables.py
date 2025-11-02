import copy
import enum
import textwrap
from typing import Self

from attrs import field
from bs4 import BeautifulSoup
from structlog import get_logger

from pbi_core.attrs import define
from pbi_core.ssas.server import (
    DISCOVER_TEMPLATE,
    BaseCommands,
    CommandData,
    ModelCommands,
    NoCommands,
    RefreshCommands,
    RenameCommands,
)
from pbi_core.ssas.server.batch import Batch
from pbi_core.ssas.server.tabular_model.tabular_model import BaseTabularModel, discover_xml_to_dict

from .base_ssas_table import SsasTable
from .enums import RefreshType

logger = get_logger()


@define()
class SsasAlter(SsasTable):
    """Class for SSAS records that implement alter functionality.

    The `alter <https://learn.microsoft.com/en-us/analysis-services/tmsl/alter-command-tmsl?view=asallproducts-allversions>`_ spec
    """  # noqa: E501

    _commands: BaseCommands

    def alter_cmd(self) -> CommandData:
        """Prepares the command data for altering an object in SSAS.

        This has been separated from the `alter` method to allow for batch commands.
        """
        return self._commands.alter.to_data(
            data=self.xml_fields(),
            db_name=self._tabular_model.db_name,
        )

    def alter(self) -> BeautifulSoup:
        """Updates a non-name field of an object in SSAS."""
        xml_command = Batch(commands=[self.alter_cmd()]).render_xml()
        logger.info("Syncing Alter Changes to SSAS", obj=self._db_type_name())
        return self.query_xml(xml_command, db_name=self._tabular_model.db_name)


@define()
class SsasRename(SsasTable):
    """Class for SSAS records that implement rename functionality.

    The `rename <https://learn.microsoft.com/en-us/analysis-services/tmsl/rename-command-tmsl?view=asallproducts-allversions>`_ spec
    """  # noqa: E501

    _commands: RenameCommands

    def rename_cmd(self) -> CommandData:
        """Prepares the command data for renaming an object in SSAS.

        This has been separated from the `rename` method to allow for batch commands.
        """
        return self._commands.rename.to_data(
            data=self.xml_fields(),
            db_name=self._tabular_model.db_name,
        )

    def rename(self) -> BeautifulSoup:
        """Updates a name field of an object in SSAS."""
        xml_command = Batch(commands=[self.rename_cmd()]).render_xml()
        logger.info("Syncing Rename Changes to SSAS", obj=self._db_type_name())
        return self.query_xml(xml_command, db_name=self._tabular_model.db_name)


@define()
class SsasCreate(SsasTable):
    """Class for SSAS records that implement create functionality.

    The `create <https://learn.microsoft.com/en-us/analysis-services/tmsl/create-command-tmsl?view=asallproducts-allversions>`_ spec
    """  # noqa: E501

    _commands: BaseCommands
    _discover_fields: tuple[str, ...] = field(factory=tuple)
    _discover_category: str = field(default="NOT_SET")

    def create_cmd(self) -> CommandData:
        """Prepares the command data for creating an object in SSAS.

        This has been separated from the `create` method to allow for batch commands.
        """
        return self._commands.create.to_data(
            data=self.xml_fields(),
            db_name=self._tabular_model.db_name,
        )

    def create(self) -> BeautifulSoup:
        """Creates a new record in the SSAS DB based on the python object."""
        xml_command = Batch(commands=[self.create_cmd()]).render_xml()
        logger.info("Syncing Create Changes to SSAS", obj=self._db_type_name())
        # We return the result of the discover because the create command only returns a success/failure response
        self._tabular_model.server.query_xml(xml_command, db_name=self._tabular_model.db_name)
        return self.discover()

    @classmethod
    def _create_helper(cls: type[Self], inst: "SsasCreate", ssas: "BaseTabularModel") -> "Self":
        """Helper method to create an instance of the class in the SSAS DB and return the remote version.

        We return the remote version to ensure we have all fields populated as they exist in SSAS.
        """
        # Set the tabular model for the measure. Has to be done separately since attrs doesn't expect it
        inst._tabular_model = ssas
        inst._original_data = None
        x = inst.create()

        # Due to the way the function was implemented, it assumes the last group is CalcDependency
        # Since we always have a single group, it will always been CalcDependency
        # It also has an extra "id" field because of this
        row_info = discover_xml_to_dict(x)["CalcDependency"][0]
        del row_info["id"]
        remote_inst = cls.model_validate(row_info)
        remote_inst._tabular_model = ssas
        remote_inst._original_data = copy.copy(remote_inst)
        return remote_inst

    def discover(self) -> BeautifulSoup:
        filter_fields = []
        for f in self._discover_fields:
            db_name = self._db_field_names[f]
            val = getattr(self, f)
            if isinstance(val, enum.Enum):
                val = val.value
            filter_fields.append(f"<{db_name}>{val}</{db_name}>")
        filter_expr = textwrap.indent("\n".join(filter_fields), " " * 8)

        xml_command = DISCOVER_TEMPLATE.render(
            db_name=self._tabular_model.db_name,
            discover_entity=self._discover_category,
            filter_expr=filter_expr,
        )
        return self._tabular_model.server.query_xml(xml_command, db_name=self._tabular_model.db_name)


@define()
class SsasDelete(SsasTable):
    """Class for SSAS records that implement delete functionality.

    The `delete <https://learn.microsoft.com/en-us/analysis-services/tmsl/delete-command-tmsl?view=asallproducts-allversions>`_ spec
    """  # noqa: E501

    _commands: BaseCommands

    def delete_cmd(self) -> CommandData:
        """Prepares the command data for deleting an object from SSAS.

        This has been separated from the `delete` method to allow for batch commands.
        """
        data = {
            "ID": self.id,
        }
        return self._commands.delete.to_data(
            data=data,
            db_name=self._tabular_model.db_name,
        )

    def delete(self) -> BeautifulSoup:
        """Removes an object from SSAS."""
        # The variation can point to at most one table
        objects_to_delete = self.delete_objects()
        cmds = [obj.delete_cmd() for obj in objects_to_delete]

        xml_command = Batch(commands=cmds).render_xml()
        logger.info("Syncing Delete Changes to SSAS", objs=objects_to_delete)
        return self.query_xml(xml_command, db_name=self._tabular_model.db_name)

    def delete_objects(self) -> frozenset["SsasDelete"]:
        """Returns a set of objects that should be deleted before this object is deleted.

        By default, there are no dependencies.
        Override this method in subclasses to provide specific dependencies.

        Note:
            We include the object itself in the returned set to ensure it gets deleted. In certain subclasses,
            we exclude the object itself since the deletion of dependencies may already cover it. For instance,
            you call the method to delete a Partition. The partition checks if it's the last partition of a table,
            and if so, it adds the table to the dependencies to be deleted. The deletion of the table will inherently
            handle the deletion of the partition, so we can't explicitly also include the partition in that case.

        """
        return frozenset({self})


@define()
class SsasRefresh(SsasTable):
    """Class for SSAS records that implement refresh functionality.

    The `refresh <https://learn.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions>`_ spec
    """  # noqa: E501

    _default_refresh_type: RefreshType
    _commands: RefreshCommands

    def refresh_cmd(self, refresh_type: RefreshType | None = None) -> CommandData:
        """Prepares the command data for refreshing an object in SSAS.

        This has been separated from the `refresh` method to allow for batch commands.
        """
        data = self.xml_fields() | {"RefreshType": (refresh_type or self._default_refresh_type).value}
        return self._commands.refresh.to_data(
            data=data,
            db_name=self._tabular_model.db_name,
        )

    def refresh(self, refresh_type: RefreshType | None = None) -> BeautifulSoup:
        xml_command = Batch(commands=[self.refresh_cmd(refresh_type)]).render_xml()
        logger.info("Syncing Refresh Changes to SSAS", obj=self)
        return self.query_xml(xml_command, db_name=self._tabular_model.db_name)


@define()
class SsasReadonlyRecord(SsasTable):
    """Class for SSAS records that implement no command."""

    _commands: NoCommands = field(init=False, repr=False, eq=False)


@define()
class SsasEditableRecord(SsasCreate, SsasAlter, SsasDelete):
    _commands: BaseCommands = field(init=False, repr=False, eq=False)


@define()
class SsasRenameRecord(SsasCreate, SsasAlter, SsasDelete, SsasRename):
    _commands: RenameCommands = field(init=False, repr=False, eq=False)  # pyright: ignore reportIncompatibleVariableOverride


@define()
class SsasRefreshRecord(SsasCreate, SsasAlter, SsasDelete, SsasRename, SsasRefresh):
    _commands: RefreshCommands = field(init=False, repr=False, eq=False)  # pyright: ignore reportIncompatibleVariableOverride


@define()
class SsasModelRecord(SsasAlter, SsasRefresh, SsasRename):
    """Solely used for the single Model record."""

    _commands: ModelCommands = field(init=False, repr=False, eq=False)  # pyright: ignore reportIncompatibleVariableOverride
