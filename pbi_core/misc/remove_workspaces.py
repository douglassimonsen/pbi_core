import shutil
from pathlib import Path

from pbi_core.ssas.setup import PbiCoreStartupConfig


def get_workspaces() -> list[Path]:
    settings = PbiCoreStartupConfig.from_file()
    if settings.workspace_dir is None:
        return []
    return list(settings.workspace_dir.iterdir())


def list_workspaces() -> None:
    settings = PbiCoreStartupConfig.from_file()
    workspaces = get_workspaces()
    if len(workspaces) == 0:
        print(f"No workspaces to remove from {settings.workspace_dir}")
    else:
        print("Folders to remove:")
        for folder in workspaces:
            print(" " * 4, folder)
        resp = input(f"Total workspaces: {len(workspaces)}. Press Y to continue: ")
        if resp.lower() != "y":
            print("Aborting")
            exit()


def clear_workspaces() -> None:
    settings = PbiCoreStartupConfig.from_file()
    workspaces = get_workspaces()
    if len(workspaces) == 0:
        print(f"No workspaces to remove from {settings.workspace_dir.absolute().as_posix()}")

    list_workspaces()

    for folder in workspaces:
        print(f"Deleting: {folder.absolute().as_posix()}")
        try:
            shutil.rmtree(folder)
        except PermissionError:
            print("\tWorkspace currently being used by an SSAS instance")
