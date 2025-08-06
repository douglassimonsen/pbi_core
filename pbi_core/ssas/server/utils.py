import pathlib

import jinja2

COMMAND_DIR: pathlib.Path = pathlib.Path(__file__).parent / "command_templates"

COMMAND_TEMPLATES: dict[str, jinja2.Template] = {
    f.name: jinja2.Template(f.read_text()) for f in COMMAND_DIR.iterdir() if f.is_file()
}
ROOT_FOLDER = pathlib.Path(__file__).parents[2]
SKU_ERROR = "ImageLoad/ImageSave commands supports loading/saving data for Excel, Power BI Desktop or Zip files. File extension can be only .XLS?, .PBIX or .ZIP."
