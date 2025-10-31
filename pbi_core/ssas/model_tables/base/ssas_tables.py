from attrs import field
from bs4 import BeautifulSoup
from structlog import get_logger

from pbi_core.attrs import define
from pbi_core.ssas.server import BaseCommands, ModelCommands, NoCommands, RefreshCommands, RenameCommands
from pbi_core.ssas.server._command_utils import CommandData
from pbi_core.ssas.server.batch import Batch

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
        return CommandData(
            data=self.xml_fields(),  # pyright: ignore[reportArgumentType]
            command=self._commands.alter,
            entity=self._db_type_name(),
            db_name=self._tabular_model.db_name,
        )

    def alter(self) -> BeautifulSoup:
        """Updates a non-name field of an object in SSAS."""
        xml_command = Batch([self.alter_cmd()]).render_xml()
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
        return CommandData(
            data=self.xml_fields(),  # pyright: ignore[reportArgumentType]
            command=self._commands.rename,
            entity=self._db_type_name(),
            db_name=self._tabular_model.db_name,
        )

    def rename(self) -> BeautifulSoup:
        """Updates a name field of an object in SSAS."""
        xml_command = Batch([self.rename_cmd()]).render_xml()
        logger.info("Syncing Rename Changes to SSAS", obj=self._db_type_name())
        return self.query_xml(xml_command, db_name=self._tabular_model.db_name)


@define()
class SsasCreate(SsasTable):
    """Class for SSAS records that implement create functionality.

    The `create <https://learn.microsoft.com/en-us/analysis-services/tmsl/create-command-tmsl?view=asallproducts-allversions>`_ spec
    """  # noqa: E501

    _commands: BaseCommands

    def create_cmd(self) -> CommandData:
        """Prepares the command data for creating an object in SSAS.

        This has been separated from the `create` method to allow for batch commands.
        """
        return CommandData(
            data=self.xml_fields(),  # pyright: ignore[reportArgumentType]
            command=self._commands.create,
            entity=self._db_type_name(),
            db_name=self._tabular_model.db_name,
        )

    def create(self) -> BeautifulSoup:
        """Creates a new SSAS object based on the python object."""
        xml_command = Batch([self.create_cmd()]).render_xml()
        logger.info("Syncing Create Changes to SSAS", obj=self._db_type_name())
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
        return CommandData(
            data=data,  # pyright: ignore[reportArgumentType]
            command=self._commands.delete,
            entity=self._db_type_name(),
            db_name=self._tabular_model.db_name,
        )

    def delete(self) -> BeautifulSoup:
        """Removes an object from SSAS."""
        # The variation can point to at most one table
        objects_to_delete = self.delete_objects()
        cmds = [obj.delete_cmd() for obj in objects_to_delete]

        xml_command = Batch(cmds).render_xml()
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
        return CommandData(
            data=data,  # pyright: ignore[reportArgumentType]
            command=self._commands.refresh,
            entity=self._db_type_name(),
            db_name=self._tabular_model.db_name,
        )

    def refresh(self, refresh_type: RefreshType | None = None) -> BeautifulSoup:
        xml_command = Batch([self.refresh_cmd(refresh_type)]).render_xml()
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
