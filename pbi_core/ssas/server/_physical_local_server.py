import pathlib
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from ...logging import get_logger

if TYPE_CHECKING:
    from _typeshed import StrPath
import atexit
import os
import shutil
import subprocess  # nosec. It's necessary to run the msmdsrv exe

import backoff
import psutil

from .utils import COMMAND_TEMPLATES, get_msmdsrv_info

logger = get_logger()
PORT_ACCESS_TRIES = 5


class SSASProcess:
    """
    This class handles the SSAS instance as a OS process

    Args:
        pid (Optional[int]): The process ID of the SSAS instance. If None, the class will create a new SSAS process
        workspace_directory (StrPath): The path to the workspace corresponding to the pid. Should only be included when the pid is not provided.
        kill_on_exit (bool): Specifies whether the SSAS instance should be terminated when the python session exits (implemented via atexit lib)

    Examples:
        .. code-block:: python
           :linenos:

           SSASProcess('tmp/workspace')  # generates a new SSAS Process and generates workspace documents at 'tmp/workspace'
           SSASProcess(4321)  # connects to an existing SSAS Process at 4321
           SSASProcess('tmp/workspace', False)  # Generates a new SSAS Process and allows it to run beyond the lifetime of the Python script

    Raises:
        ValueError: If both or none of ``pid`` and ``workspace_directory`` are specified

    """

    _workspace_directory: pathlib.Path
    pid: int = -1
    kill_on_exit: bool

    def __init__(
        self, pid: Optional[int] = None, workspace_directory: Optional["StrPath"] = None, kill_on_exit: bool = True
    ):
        """
        __init__ is not intended to be directly called. This class is
        expected to be initialized from the .from_pid or .new_instance methods
        """
        self.kill_on_exit = kill_on_exit
        atexit.register(self._on_exit)

        if pid is None:
            if workspace_directory is None:
                raise ValueError("If the pid is not specified, you must specify a workspace directory")
            self._workspace_directory = pathlib.Path(workspace_directory)
            logger.info(
                "No pid provided. Initializing new SSAS Instance",
                workspace_dir=self.workspace_directory(),
                msmdsrv_exe=self.powerbi_exe_path,
            )
            self.pid = self.initialize_server()
        else:
            if workspace_directory is not None:
                raise ValueError("If the pid is specified, you must not specify a workspace directory")
            self.pid = pid
            self._workspace_directory = self._get_workspace_directory()

    def _get_workspace_directory(self) -> pathlib.Path:
        """
        Uses the PID and the command used to initialize that PID to identify the workspace directory used by the SSAS process
        """
        proc = psutil.Process(self.pid)
        proc_info = get_msmdsrv_info(proc)
        if proc_info is None:
            raise ValueError("This PID doesn't correspond to a valid SSAS instance")
        return proc_info.workspace_directory

    def workspace_directory(self) -> pathlib.Path:
        return pathlib.Path(self._workspace_directory).absolute()

    @cached_property
    def powerbi_exe_path(self) -> str:
        """
        Tests locations on your computer for the ``msmdsrv.exe`` file needed to create an SSAS process

        Returns:
            str: the absolute POSIX path to the msmdsrv exe on the system.

        Raises:
            FileNotFoundError: when no ``msmdsrv.exe`` file is found in any of the candidate folders
        """
        candidate_folders = ["C:/Program Files/Microsoft Power BI Desktop", "C:/Program Files/WindowsApps"]
        for folder in candidate_folders:
            for path in pathlib.Path(folder).glob("**/msmdsrv.exe"):
                logger.debug("Found exe path", path=path.absolute().as_posix())
                return path.absolute().as_posix()
        raise FileNotFoundError("Cannot find msmdrsv.exe to run SSAS")

    @property
    def certificate_directory(self) -> str:
        """
        The certificate directory needs to be identified for intiializing the SSAS instance.
        Since this string is being passed to a config used by microsoft products, we follow Windows
        "\\" convention for directories
        """
        return rf"C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Power BI Desktop\CertifiedExtensions"

    def create_workspace(self) -> None:
        """
        Creates the workspace directory and populates the initial config file for the new SSAS instance
        """
        logger.debug("initializing SSAS Workspace", directory=self.workspace_directory())
        self.workspace_directory().mkdir(parents=True, exist_ok=True)
        (self.workspace_directory() / "msmdsrv.ini").write_text(
            COMMAND_TEMPLATES["msmdsrv.ini"].render(
                data_directory=self.workspace_directory().absolute().as_posix().replace("/", "\\"),
                certificate_directory=self.certificate_directory,
            )
        )

    def run_msmdsrv(self) -> int:
        """
        Commands are explained here: https://stackoverflow.com/q/36458981
        -c: console mode
        -n "instance_name": instance name (the name of the default database)
        -s "workspace_directory": The location of the configuration

        Note:
            ``-s`` points to the workspace created in the method "create_workspace"
        """
        logger.debug("Running msmdsrv exe")
        command = [  # pbi_core_master is not really used, but a port file isn't generated without it
            self.powerbi_exe_path,
            "-c",
            "-n",
            "pbi_core_master",
            "-s",
            self.workspace_directory().as_posix(),
        ]
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=flags,
        ).pid  # nosec. It's necessary to run the msmdsrv exe

    @cached_property
    @backoff.on_exception(backoff.expo, FileNotFoundError, max_time=5)
    def port(self) -> int:
        """
        We include exponential backoff in this function since it occasionally takes 1-3 seconds for msmdsrv.exe
        to generate the msmdsrv.port.txt file in the workspace

        Raises:
            FileNotFoundError: when ``msmdsrv.port.txt`` cannot be found in the SSAS workspace folder
        """
        try:
            return int((self.workspace_directory() / "msmdsrv.port.txt").read_text(encoding="utf-16-le"))
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Could not find msmdsrv.port.txt file in directory {self.workspace_directory()}. This is needed to get the port of the SSAS instance"
            ) from e

    def initialize_server(self) -> int:
        self.create_workspace()
        return self.run_msmdsrv()

    def _on_exit(self) -> None:
        if self.kill_on_exit:
            self.terminate()

    @staticmethod
    @backoff.on_exception(backoff.expo, ValueError, max_time=10)
    def wait_until_terminated(process: psutil.Process) -> None:
        """
        Takes a process class and checks if the process is still running
        """
        if process.is_running():
            raise ValueError("The process will not terminate")

    def terminate(self) -> None:
        """
        Kills the SSAS instance.

        The code performs the following:

        1. Checks the PID. If the PID isn't associated with an active process, we declare the SSAS instance killed
        2. Checks the information associated with the PID (from ``get_msmdsrv_info``). If it's not running ``msmdsrv.exe`` with active ports, we consider it killed
        3. We call a terminate command
        4. We wait until the command is in a non-running state
        5. We then remove the corresponding workspace
        """
        try:
            p = psutil.Process(self.pid)
        except psutil.NoSuchProcess:  # something else killed it??
            logger.info("SSAS Proc already terminated", pid=self.pid)
            return
        except ValueError:
            logger.info("SSAS Proc never initialized", pid=self.pid)
            return
        if not get_msmdsrv_info(p):  # indicates another process has already taken this PID
            return
        p.terminate()
        self.wait_until_terminated(p)
        logger.info("Terminated SSAS Proc", pid=self.pid)

        shutil.rmtree(self.workspace_directory(), ignore_errors=True)
        logger.info("Workspace Removed", directory=self.workspace_directory().as_posix())
