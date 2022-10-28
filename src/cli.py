from backend import (
    ModPack,
    ModPackError,
    CompatableProgressBar,
    InternalModPackError,
    ModPackNotFoundError,
)

from rich.console import Console
from rich.traceback import install
from alive_progress import alive_bar

import click
import random
import time

c = Console()
install(console=c, show_locals=True, extra_lines=4)

@click.command(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)
@click.argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.argument("output_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("-c", "--chunk-size", type=int, default=1024, help="Chunk size for downloads")
@click.option("-d","--download-optional", is_flag=True, default=True, help="Download optional files")
@click.option("--no-clean", is_flag=True, default=False, help="Don't delete temp directory after install")


class ProgressBar(CompatableProgressBar):
    def __init__(self):
        self._init_()
        self.bar = alive_bar()


    def setTotalValue(self, value: int):
        self.bar.update(value)  # type: ignore

    def step(self):
        self.bar()  # type: ignore

    def set(self, value: int):
        self.bar.update(value)  # type: ignore

def cli(path: str, chunk_size: int, output_dir: str, download_optional: bool, no_clean: bool):
    try:
        with alive_bar() as bar:
            _temp_bar = ProgressBar()
            _temp_bar._init_()
            modpack = ModPack(
                console=c,
                download_optional_mods=download_optional,
                keep_files=no_clean,
                output_dir=output_dir,
                path=path,
                progress_bar_current=ProgressBar(),
                progress_bar_overall=_temp_bar,
            )
            modpack.install()
            if not no_clean:
                modpack.clean()
    except ModPackError:
        c.print_exception()
        c.print("[red]An error occured, please report this to the developer[/red]")

    except InternalModPackError:
        c.print_exception()
        c.print("[red]An error occured, please report this to the developer[/red]")

    except ModPackNotFoundError:
        c.print_exception()
        c.print("[red]An error occured, please report this to the developer[/red]")

cli() # type: ignore