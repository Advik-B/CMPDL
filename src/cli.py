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
install(console=c, show_locals=True, extra_lines=4)

@click.command(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)
@click.argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.argument("output_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("-c", "--chunk-size", type=int, default=1024, help="Chunk size for downloads")
@click.option("-d","--download-optional", is_flag=True, default=True, help="Download optional files")
@click.option("--no-clean", is_flag=True, default=False, help="Don't delete temp directory after install")

def cli(path: str, chunk_size: int, output_dir: str, download_optional: bool, no_clean: bool):
    pass

cli()