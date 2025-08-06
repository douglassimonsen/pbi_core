import dataclasses

import jinja2


@dataclasses.dataclass
class NoCommands:
    pass


@dataclasses.dataclass
class SsasBaseCommands(NoCommands):
    alter: jinja2.Template
    create: jinja2.Template
    delete: jinja2.Template


@dataclasses.dataclass
class SsasRenameCommands(SsasBaseCommands):
    rename: jinja2.Template


@dataclasses.dataclass
class SsasRefreshCommands(SsasRenameCommands):
    refresh: jinja2.Template


@dataclasses.dataclass
class SsasModelCommands:
    alter: jinja2.Template
    refresh: jinja2.Template
    rename: jinja2.Template


SsasCommands = SsasBaseCommands | SsasRenameCommands | SsasRefreshCommands | SsasModelCommands
