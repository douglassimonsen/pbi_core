from pathlib import Path

from pydantic import BaseModel


class PbyxConfig(BaseModel):
    adomd_clientpath: Path
    msmdsrv_ini: Path
    workspace_dir: Path


if __name__ == "__main__":
    x = PbyxConfig(
        adomd_clientpath="",
        msmdsrv_ini="",
        workspace_dir="",
    ).model_dump_json(indent=2)
    print(x)
