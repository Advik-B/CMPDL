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

c = Console()
install(console=c, extra_lines=5, show_locals=True, indent_guides=True)

class ProgressBar(CompatableProgressBar):
    def __init__(self):
        self._init_()
        self.progress = Progress(console=c)
        self.task = self.progress.add_task("Downloading", total=self.total)
        self.progress.start()
        self.progress.update(self.task, total=self.total)

    def step(self, val: int = 1):
        super().step(val)

        self.progress.update(self.task, completed=self.value)
        self.progress.refresh()


    def setTotalValue(self, val: int):
        super().setTotalValue(val)

        self.progress.update(self.task, total=val, completed=self.value)
        self.progress.refresh()

    def set(self, val: int):
        super().set(val)
        self.progress.update(self.task, completed=self.value)
        self.progress.refresh()

m = ModPack(
    console=c,
    download_optional_mods=True,
    keep_files=True,
    progress_bar_overall=CompatableProgressBar(),
    progress_bar_current=ProgressBar(),
    path="sample.manifest.zip",
    output_dir="output",
)
m.initilize()
m.install()
m.clean()