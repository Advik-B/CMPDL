from v import api_key
from curseforge import CurseClient
from rich.console import Console
from rich.progress import Progress
from multiprocessing import Pool
from time import perf_counter as now # Benchmarking
from requests import get

import json
import os

def main():
    CLIENT = CurseClient(api_key, cache=True)
    console = Console()
    pbars = Progress(console=console, transient=True)
    bars = [pbars.add_task(f"Downloading mod {i}", total=100) for i in range(10)]

    for i in range(10):
        pbars.update(bars[i], advance=10)

if __name__ == "__main__":
    main()
