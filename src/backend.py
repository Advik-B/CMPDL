from cursepy import CurseClient
from tree_generator import gentree
from time import perf_counter as now
from rich.console import Console  # For type hinting
from urllib.parse import unquote

import v
import os
import json
import zipfile
import shutil
import tempfile
import requests


class CompatableProgressBar:
    """A general scaffold class for creating a progress bar to work with the backend"""

    def _init_(self):
        self.value = 0
        self.total = 0

    def step(self, val: int = 1):
        self.value += val
        if self.value > self.total:
            self.value = self.total

    def setTotalValue(self, val: int):
        self.total = val

    def set(self, val: int):
        self.value = val
        if self.value > self.total:
            self.value = self.total


class ModPackError(Exception):
    """A general exception for modpack errors, usally caused by the user"""

    pass


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
        progress_bar_overall: CompatableProgressBar,
        progress_bar_current: CompatableProgressBar,
        download_optional_mods: bool = False,
        keep_files: bool = False,
        chunk_size: int = 1024,
    ):
        self.log = console.log
        self.keep_config: bool = keep_files
        self.path: str = path
        self.output_dir: str = output_dir
        self.optional_mod: bool = download_optional_mods

        self.progress_bar_overall: CompatableProgressBar = progress_bar_overall
        self.progress_bar_current: CompatableProgressBar = progress_bar_current

        self.seperator = "="

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

        self.console = console
        self.chunk_size = chunk_size

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

        self.curseClient = CurseClient(v.api_key)
        # self.opendtemp()  # TODO: Remove this in production
        self.initilized = True

    def makedtemp(self) -> str:
        """Make a temporary directory and return the path to it"""
        self.tempdir = tempfile.mkdtemp(prefix="CMPDL.TEMPORARY.")
        return self.tempdir

    def opendtemp(self):
        os.system("explorer " + self.tempdir)

    def _ZIP(self):
        self.makedtemp()
        self.log(
            f"Extracting [bold green]ZIP[/] file [b]{self.filename}[/] to [b yellow]{self.tempdir}[/]"
        )
        with zipfile.ZipFile(self.path, "r") as zip_:
            zip_.extractall(self.tempdir)

        self.log(gentree(self.tempdir))

    def _DIR(self):
        self.makedtemp()
        self.log(
            f"Copying [b green]DIR[/] [b]{self.path}[/] to [b yellow]{self.tempdir}[/]"
        )
        O = shutil.copytree(self.path, self.tempdir)
        self.log(gentree(O))

    def _JSON(self): pass

    def install(self):
        if not self.initilized:
            raise InternalModPackError("ModPack not initilized")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            self.manifest_path = os.path.join(self.tempdir, "manifest.json")
        except AttributeError:
            self.manifest_path = self.path

        # Read the manifest file
        self.log(f"Reading [b green]manifest[/] file [b]{self.manifest_path}[/]")
        try:
            manifest = json.load(open(self.manifest_path, "r"))
        except json.decoder.JSONDecodeError as e:
            raise ModPackError("Invalid manifest file") from e

        except FileNotFoundError as e:
            manifest = json.load(open(self.path, "r"))

        # This codeblock iterates through the files and gets the actual length of the files
        # (Not the length of the list)
        total = len(manifest["files"])  # Allegedly the total number of files
        if self.optional_mod is False:
            # execute ONLY if:
            # The user does not want to download optional mods
            for _ in manifest["files"]:
                # "_" is the current file
                if _["optional"]:  # If the file is optional
                    total -= 1  # Subtract 1 from the total
        # --------------------------------------
        self.log(
            f"Installing [b green]{self.method}[/] modpack [b]{self.filename}[/] to [b yellow]{self.output_dir}[/]"
        )

        self.progress_bar_overall.setTotalValue(total)
        self._iter_manifest(manifest, total)  # Main installation function

    def _iter_manifest(self, manifest: dict, total: int):

        for index, _mod in enumerate(manifest["files"]):
            mod= self.curseClient.addon(_mod["projectID"])
            self.log(
                f"Downloading [b green]{mod.name}[/] ({mod.id}) [b]{index + 1}[/] of [b]{total}[/]"
            )
            self.log(f"Mod name: {mod.name}")
            self.log(f"Mod ID: {mod.id}")
            _names = ""
            for _name in mod.authors:
                _names += _name.name + ", "
            self.log(f"Mod author(s): {_names[:-2] if _names else 'Unknown'}")
            if _mod["required"]:
                self.log(f"Mod is [b green]required[/]")
                file = mod.file(_mod["fileID"])
                save_path = os.path.join(
                    self.output_dir, unquote(file.download_url.split("/")[-1])
                )
                self.download(file.download_url, save_path, self.progress_bar_current)
                self.progress_bar_current.set(0)

    def clean(self):
        if self.method == "ZIP" or self.method == "DIR":
            self.log(f"Deleting [b red]temp[/] directory [b yellow]{self.tempdir}[/]")
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def download(self, url: str, path: str, progress_bar: CompatableProgressBar):
        if not self.initilized:
            raise Exception("ModPack not initialized")

        r = requests.get(url, stream=True)
        with open(path, "wb") as f:
            self.log(f"URL: {url}")
            total_length = int(r.headers.get("content-length"))  # type: ignore
            self.log(f"TOTAL LENGTH: {total_length}")
            progress_bar.setTotalValue(total_length)
            for chunk in r.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    progress_bar.step()


# Test code
if __name__ == "__main__":
    from rich.traceback import install

    install(extra_lines=5, show_locals=True)
    console = Console()
    console.log("Testing the modpack class")
    _p1 = CompatableProgressBar()
    _p1._init_()  # Get the progress bar ready
    _p2 = CompatableProgressBar()
    _p2._init_()  # Get the progress bar ready
    mpack = ModPack(
        path="sample.manifest.zip",
        console=console,
        download_optional_mods=True,
        keep_files=True,
        progress_bar_overall=_p1,
        progress_bar_current=_p2,
        # HACK: This is just a trick to make it think it's a progress bar
        output_dir="output",
    )
    mpack.initilize()
    mpack.install()
    mpack.clean()
    # mpack.clean() # Uncomment this to clean up the temp directory (recommended)
