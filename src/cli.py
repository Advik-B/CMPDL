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
from threading import Thread

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

    pmb = per_mod_bar()
    ob = overall_bar()
    m = ModPack(
        "sample.manifest.zip",
        console=c,
        output_dir="output",
        progress_bar_overall=pmb,
        progress_bar_current=ob,
        download_optional_mods=True,
        )
    def _refresh_progresss():
        while True:
            progress.update(per_mod, completed=pmb.value, total=pmb.total)
            progress.update(overall, completed=ob.value, total=ob.total)
            progress.refresh()


    Thread(target=_refresh_progresss, daemon=True).start()

    m.initilize()
    m.install()
    m.clean()
