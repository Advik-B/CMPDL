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

class CompatableProgressBar:
    """A general scaffold class for creating a progress bar to work with the backend"""
    def step(self, val: int=1): pass

class ModPackNotFoundError(Exception):
    """This error is raised when a modpack is not found on the local path provided by the user"""

class InternalModPackError(Exception):
    """This error is raised when the ModPack class encounters an error that is not the user's fault"""

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
        methods = {
            "ZIP": self._ZIP,
            "DIR": self._DIR,
            "JSON": self._JSON,
        }
        try:
            # Call the method based on the method name string (self.method) (usally not buggy)
            methods[self.method]()
        except KeyError as e:
            raise InternalModPackError(f"Invalid method {self.method}") from e

    def _ZIP(self):
        self.tempdir = tempfile.mkdtemp(prefix="CMPDL~")
        self.log(f"Extracting [bold green]ZIP[/] file [b]{self.filename}[/] to [b yellow]{self.tempdir}[/]")
        with zipfile.ZipFile(self.path, "r") as zip_:
            zip_.extractall(self.tempdir)

        self.log(gentree(self.tempdir))
        os.system("explorer " + self.tempdir) #TODO: Remove this in production

    def _DIR(self):
        self.tempdir = tempfile.mkdtemp(prefix="CMPDL~")
        O = shutil.copytree(self.path, self.tempdir)
        self.log(gentree(O))
        os.system("explorer " + self.tempdir) #TODO: Remove this in production

    def _JSON(self): pass

    def clean(self):
        if self.method == "ZIP" or self.method == "DIR":
            self.log(f"Deleting [b red]temp[/] directory [b yellow]{self.tempdir}[/]")
            shutil.rmtree(self.tempdir, ignore_errors=True)

if __name__ == "__main__":
    console = Console()
    console.log("Testing the modpack class")
    mpack = ModPack(path="sample.manifest.zip",
                    console=console,
                    download_optional_mods=True,
                    keep_files=True,
                    output_dir="output")
    mpack.initilize()
    # mpack.clean() # Uncomment this to clean up the temp directory (recommended)
