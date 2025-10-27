import textwrap
from pathlib import Path

import jinja2
from attrs import fields

from pbi_core.attrs import BaseValidation, define
from pbi_core.logging import get_logger

logger = get_logger()

PACKAGE_DIR = Path(__file__).parents[2]
assert PACKAGE_DIR.name == "pbi_core"


@define()
class PbiCoreStartupConfig(BaseValidation):
    workspace_dir: Path
    cert_dir: Path | None = None
    msmdsrv_ini: Path | None = None
    msmdsrv_exe: Path | None = None
    desktop_exe: Path | None = None

    @staticmethod
    def from_file(path: Path | None = None) -> "PbiCoreStartupConfig":
        path = path or Path(__file__).parents[2] / "local" / "settings.json"
        return PbiCoreStartupConfig.model_validate_json(path.read_text())

    def __attrs_post_init__(self) -> None:
        for a in fields(self.__class__):
            val: Path = getattr(self, a.name)
            if val is not None and not val.is_absolute():
                val = PACKAGE_DIR / val
            setattr(self, a.name, val)

    def msmdsrv_ini_template(self) -> jinja2.Template:
        assert self.msmdsrv_ini is not None
        return jinja2.Template(self.msmdsrv_ini.read_text())


def get_startup_config() -> PbiCoreStartupConfig:
    config_path = PACKAGE_DIR / "local" / "settings.json"
    try:
        logger.info("Loading startup configuration", path=config_path)
        with config_path.open("r") as f:
            cfg = PbiCoreStartupConfig.model_validate_json(f.read())
            logger.info("Loaded startup configuration", path=config_path)
            return cfg
    except FileNotFoundError as e:
        logger.exception("Startup configuration not found", path=config_path)
        msg = textwrap.dedent("""

        When loading a pbix file with pbi_core, the package needs one of the following:
            1. The package needs to be initialized once with "python -m pbi_core setup" to find the necessary SSAS
               files (currently broken)
            2. To be run while PowerBI Desktop is currently running, so that the SSAS server set up by PowerBI Desktop
               can be used
            3. The load_pbix function can be called with the `load_ssas=False` argument, which will not load the SSAS
               model and therefore not require the SSAS server to be set up.
        """)
        raise FileNotFoundError(msg) from e
