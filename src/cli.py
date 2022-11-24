from backend import (
    ModPack,
    ModPackError,
    CompatableProgressBar,
    InternalModPackError,
    ModPackNotFoundError,
)

from rich.console import Console
from rich.traceback import install
from rich.progress import Progress, TaskID, BarColumn, TimeRemainingColumn

import click

c = Console()
install(console=c, show_locals=True, extra_lines=4)


class ProgressBar(CompatableProgressBar):
    def __init__(self):
        self.barColumn = BarColumn(bar_width=c.width - 40)
        self.timeRemainingColumn = TimeRemainingColumn()
        self.progress = Progress(
            "[progress.description]{task.description}",
            self.barColumn,
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            "ETA:",
            self.timeRemainingColumn,
            console=c,
        )
        self.task: TaskID | None = None
        self.firstTime = True

    def setTotalValue(self, val: int):
        super().setTotalValue(val)
        self.value = 0
        self.progress.start()
        if self.firstTime:
            self.firstTime = False
            self.task = self.progress.add_task(
            "Downloading Mod", total=val // 1024,)
            self.progress.update(self.task, advance=0)
        else:
            # Remove the old task
            self.progress.remove_task(self.task) # type: ignore
            self.task = self.progress.add_task(
            "Downloading Mod", total=val // 1024,)
            self.progress.update(self.task, advance=0)

    def step(self, val: int = 1):
        super().step(val)
        self.progress.update(self.task, advance=val)  # type: ignore

    def set(self, val: int):
        super().set(val)

class OverallProgressBar(CompatableProgressBar):

    def __init__(self) -> None:
        self._init_()
        self.barColumn = BarColumn(bar_width=c.width - 40)
        self.timeRemainingColumn = TimeRemainingColumn()
        self.progress = Progress(
            "[progress.description]{task.description}",
            self.barColumn,
            "[progress.percentage]{task.percentage:>3.0f}%",
            "-",
            "ETA:",
            self.timeRemainingColumn,
            console=c,
        )
        self.task: TaskID | None = None

    def setTotalValue(self, val: int):
        super().setTotalValue(val)
        self.value = 0
        self.progress.start()
        self.task = self.progress.add_task("Installing Modpack",total=val // 1024,)
        self.progress.update(self.task, advance=0)

    def step(self, val: int = 1):
        super().step(val)
        self.progress.update(self.task, advance=val) # type: ignore

    def set(self, val: int):
        super().set(val)

def printDeveloperMessage(c: Console):
    c.print("[red]An error occured, please report this to the developer[/]")
    c.print("[italic cyan]https://github.com/Advik-B/CMPDL/issues[/]")

@click.command(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)
@click.argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.argument("output_dir", type=click.Path(file_okay=False, dir_okay=True))
@click.option("-c", "--chunk-size", type=int, default=1024, help="Chunk size for downloads")
@click.option("-d","--download-optional", is_flag=True, default=True, help="Download optional files")
@click.option("--no-clean", is_flag=True, default=False, help="Don't delete temp directory after install")
def cli(path: str, chunk_size: int, output_dir: str, download_optional: bool, no_clean: bool):
    try:
        _temp_bar = CompatableProgressBar()
        _temp_bar._init_()
        modpack = ModPack(
                console=c,
                download_optional_mods=download_optional,
                keep_files=no_clean,
                output_dir=output_dir,
                path=path,
                progress_bar_current=ProgressBar(),
                progress_bar_overall=_temp_bar,
                chunk_size=chunk_size,
            )
        modpack.initilize()
        modpack.install()
        if not no_clean:
            modpack.clean()

    except ModPackError:
        c.print_exception()
        printDeveloperMessage(c)

    except InternalModPackError:
        c.print_exception()
        printDeveloperMessage(c)

    except ModPackNotFoundError:
        c.print_exception()
        printDeveloperMessage(c)

    except Exception:
        c.print_exception()
        printDeveloperMessage(c)


cli() # type: ignore
