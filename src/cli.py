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

