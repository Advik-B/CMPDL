from backend import (
    ModPack,
    ModPackError,
    CompatableProgressBar,
    InternalModPackError,
    ModPackNotFoundError,
)

from rich.console import Console
from rich.progress import Progress
from rich.traceback import install

import click
import random
import time

c = Console()
install(console=c, extra_lines=5, show_locals=True, indent_guides=True)

with Progress(transient=True) as progress:
    overall = progress.add_task("[b green]Overall[/]-[cyan]Progress[/]", total=1)
    per_mod = progress.add_task("[b yellow]Individual[/]-[cyan]Progress[/]", total=1)

    class per_mod_bar(CompatableProgressBar):
        def __init__(self) -> None:
            super().__init__()
            self._init_()

        def setTotalValue(self, val):
            super().setTotalValue(val)
            progress.update(per_mod, total=val)

        def step(self, val: int = 1):
            super().step(val)
            progress.update(per_mod, advance=val)

    class overall_bar(CompatableProgressBar):
        def __init__(self) -> None:
            super().__init__()
            self._init_()

        def setTotalValue(self, val):
            super().setTotalValue(val)
            progress.update(overall, total=val)

        def step(self, val: int = 1):
            super().step(val)
            progress.update(overall, advance=val)

    m = ModPack(
        "sample.manifest.zip",
        console=c,
        output_dir="output",
        progress_bar_overall=per_mod_bar(),
        progress_bar_current=overall_bar(),
        download_optional_mods=True,
        )
    m.initilize()
    m.install()
    m.clean()
