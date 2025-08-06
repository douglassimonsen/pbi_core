import json
import shutil
from pathlib import Path

from pbi_core.setup.main import PbyxConfig

settings_path = Path(__file__).parents[1] / "user_settings.json"
settings = PbyxConfig.model_validate(json.load(settings_path.open("r")))


def get_workspaces() -> list[Path]:
    return list(settings.workspace_dir.iterdir())


def list_workspaces() -> None:
    workspaces = get_workspaces()
    if len(workspaces) == 0:
        print(f"No workspaces to remove from {settings.workspace_dir.absolute().as_posix()}")
    for folder in workspaces:
        print(folder)


def clear_workspaces() -> None:
    workspaces = get_workspaces()
    if len(workspaces) == 0:
        print(f"No workspaces to remove from {settings.workspace_dir.absolute().as_posix()}")

    for folder in workspaces:
        print(f"Deleting: {folder.absolute().as_posix()}")
        shutil.rmtree(folder)
