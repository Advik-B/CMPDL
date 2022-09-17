from cursepy import CurseClient
from tree_generator import gentree
from time import perf_counter as now
from rich.console import Console # For type hinting
from urllib.parse import unquote

import v
import os
import json
import zipfile
import shutil
import tempfile

class CompatableProgressBar:
    """A general scaffold class for creating a progress bar to work with the backend"""

    def _init_(self):
        self.value = 0
        self.total = 0


    def step(self, val: int=1):
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

    def makedtemp(self) -> str:
        """Make a temporary directory and return the path to it"""
        self.tempdir = tempfile.mkdtemp(prefix="CMPDL.TEMPORARY.")
        return self.tempdir

    def opendtemp(self):
        os.system("explorer " + self.tempdir)

    def _ZIP(self):
        self.makedtemp()
        self.log(f"Extracting [bold green]ZIP[/] file [b]{self.filename}[/] to [b yellow]{self.tempdir}[/]")
        with zipfile.ZipFile(self.path, "r") as zip_:
            zip_.extractall(self.tempdir)

        self.log(gentree(self.tempdir))
        self.opendtemp() #TODO: Remove this in production

    def _DIR(self):
        self.makedtemp()
        self.log(f"Copying [b green]DIR[/] [b]{self.path}[/] to [b yellow]{self.tempdir}[/]")
        O = shutil.copytree(self.path, self.tempdir)
        self.log(gentree(O))
        self.opendtemp() #TODO: Remove this in production

    def _JSON(self):
        self.makedtemp()
        self.log(f"Copying [b green]JSON[/] [b]{self.path}[/] to [b yellow]{self.tempdir}[/]")
        shutil.copy(self.path, self.tempdir)
        self.log(gentree(self.tempdir))
        self.opendtemp() #TODO: Remove this in production

    def install(self):
        if not self.initilized:
            raise InternalModPackError("ModPack not initilized")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.manifest_path = os.path.join(self.tempdir, "manifest.json")

        # Read the manifest file
        self.log(f"Reading [b green]manifest[/] file [b]{self.manifest_path}[/]")
        try:
            self.manifest = json.load(open(self.manifest_path, "r"))
        except json.decoder.JSONDecodeError as e:
            raise ModPackError("Invalid manifest file") from e

        total = len(self.manifest["files"])
        if self.optional_mod is False:
            for _ in self.manifest["files"]:
                if _["optional"]:
                    total -= 1
        self.log(f"Installing [b green]{self.method}[/] modpack [b]{self.filename}[/] to [b yellow]{self.output_dir}[/]")

        self.progress_bar_overall.setTotalValue(total)
        for index, _mod in enumerate(self.manifest):
            mod = self.curseClient.addon(_mod["projectID"])
            self.log(f"Downloading [b green]{mod.name}[/] ({mod.id}) [b]{index + 1}[/] of [b]{total}[/]")
            self.log(f"Mod name: {mod.name}")
            self.log(f"Mod ID: {mod.id}")
            self.log(f"Mod author(s): {str(mod.authors)}")
            if mod_["required"]:
                self.log(f"Mod is [b green]required[/]")
                file = mod.file(mod_["fileID"])
                save_path = os.path.join(
                    self.output_dir,
                    unquote(
                        file.download_url.split("/")[-1]
                    )
                )
                self.download(file.download_url, save_path, self.progress_bar_current)
                self.progress_bar_current.set(0)
                self.log(f"{self.seperator * os.get_terminal_size().columns}")



    def clean(self):
        if self.method == "ZIP" or self.method == "DIR":
            self.log(f"Deleting [b red]temp[/] directory [b yellow]{self.tempdir}[/]")
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def download(self, url: str, path: str, progress_bar: CompatableProgressBar):
        if not self.ini:
            raise Exception("ModPack not initialized")

        r = requests.get(link, stream=True)
        with open(path, "wb") as f:
            self.log(f"LINK: {link}")
            self.log(f"PATH: {path}")
            self.log(f"HEADERS: {r.headers}")
            total_length = int(r.headers.get("content-length"))
            self.log(f"TOTAL LENGTH: {total_length}")
            progress_bar.setTotalValue(total_length)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    progress_bar.step()
        self.log(f"Downloaded {link} to %s" % path.replace("\\", "/"))

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
