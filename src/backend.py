from cursepy import CurseClient
from tree_generator import gentree
from time import perf_counter as now
from rich.console import Console # For type hinting

import v
import os
import json
import zipfile
import shutil
import tempfile

class ModPackNotFoundError(Exception): pass

class ModPack:
    def __init__(
        self,
        path: str,
        console: Console,
        output_dir: str,
        download_optional_mods: bool = False,
        keep_files: bool = False,
        ):
        self.log = console.log
        self.keep_config: bool = keep_files
        self.path: str = path
        self.output_dir: str = output_dir
        self.optional_mod: bool = download_optional_mods

        if "/" in self.path:
            self.filename: str = self.path.split("/")[-1]
        elif "\\" in self.path:
            self.filename: str = self.path.split("\\")[-1]
        else:
            self.filename: str = self.path


        self.initilized = False
        if os.path.isdir(self.path):
            self.method = "DIR"

        elif os.path.isfile(self.path):
            if self.path.endswith(".zip"):
                self.method = "ZIP"
            elif self.path.endswith(".json"):
                self.method = "JSON"

        elif not os.path.exists(self.path):
            raise ModPackNotFoundError(f"Modpack not found at {self.path}")

    def initilize(self):
        self.log(f"Using the [b green]{self.method}[/] method")

    def _ZIP(self):
        self.tempdir = tempfile.mkdtemp(prefix="CMPDL")
        self.log(f"Extracting [green]zip[/] file [b]{self.filename}[/] to [b yellow]{self.tempdir}[/]")
        with zipfile.ZipFile(self.path, "r") as zip_:
            zip_.extractall(self.tempdir)

    def cleanUP(self):
        if self.method == "ZIP" or self.method == "DIR":
            self.log(f"Deleting [b red]temp[/] directory [b yellow]{self.tempdir}[/]")
            shutil.rmtree(self.tempdir)