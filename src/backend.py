from cursepy import CurseClient as CTClient
from tree_generator import gentree
from urllib.parse import unquote
from clint.textui import progress
from PyQt5.QtWidgets import QProgressBar
from time import perf_counter as now
import zipfile
import tempfile
import os
import json
import shutil
import requests
import v


class ModPack:
    def __init__(self, path: str, **kwargs) -> None:
        self.log = kwargs.get("log_func")
        self.secondry_log = kwargs.get("secondry_log")
        # Set up the progress bar
        self.progressbar = kwargs.get("pbar")
        self.progressbar.setValue(0)

        self.sec_progressbar = QProgressBar(kwargs.get("pbar2"))
        self.output_dir = kwargs.get("output_dir")
        self.download_optional = kwargs.get("download_optional_mods")
        self.keep_config = kwargs.get("keep_config")

        self.ini = False
        self.path = path

    def step(self, pbar: QProgressBar, value: int):
        # Send the signal to the progress bar instead of directly updating it to avoid the progress bar from freezing
        pass # Not Inplemented (yet)


    def init(self):
        self.log("Initializing Curse client...", "info")
        start = now()
        self.c = CTClient(v.api_key)
        stop = now()
        self.log(
            f"Successfully initialized Curse client in {str(stop - start)} seconds",
            "info",
        )

        del stop, start
        self.log("Initializing ModPack...", "info")
        start = now()
        if self.path.endswith(".zip"):
            self.tempdir = tempfile.mkdtemp(prefix="CMPDL")
            self.log(f"Extracting modpack to {self.tempdir}", "info")
            with zipfile.ZipFile(self.path, "r") as z:
                z.extractall(self.tempdir)
            self.log("Successfully extracted modpack", "info")
            self.log("ModPack file structure:\n%s" % gentree(self.tempdir), "info")
            self.manifest_path = os.path.join(self.tempdir, "manifest.json")
            self.meth = "ZIP"
        elif self.path.endswith(".json"):
            self.manifest_path = self.path
            self.meth = "JSON"
        try:
            self.log(f"Manifest path set to {self.manifest_path}", "info")
        except AttributeError:
            self.log("Manifest path not set", "info")

        self.log("Loading manifest...", "info")
        with open(self.manifest_path, "r") as f:
            mani = json.load(f)
        self.manifest = mani["files"]
        self.log(f'Minecraft version: {mani["minecraft"]["version"]}', "info")
        self.log(f'Modpack version: {mani["version"]}', "info")
        self.log(f'Modpack name: {mani["name"]}', "info")
        self.log(f'Modpack author(s): {mani["author"]}', "info")
        self.log(f'Modpack description: {mani.get("description")}', "info")
        self.log(f'Modpack website: {mani.get("website")}', "info")
        self.log(
            f'Modpack modloader: {mani["minecraft"]["modLoaders"][0]["id"]}',
            "info",
        )

        self.log(f'Modpack config/overrides: {mani["overrides"]}', "info")
        self.log("Successfully loaded manifest", "info")
        if self.meth == "ZIP":
            self.override_folder = os.path.join(self.tempdir, mani["overrides"])
        del mani
        stop = now()
        self.log(
            f"Successfully initialized ModPack in {str(stop - start)} seconds",
            "info",
        )

        del stop, start
        self.ini = True

    def install(self):
        global mods_folder
        self.log("Installing ModPack...", "info")
        start = now()
        if self.meth == "ZIP" and os.path.isdir(self.override_folder):

            self.log(f"Extracting overrides to {self.output_dir}", "info")
            for file in os.listdir(self.override_folder):
                if os.path.isfile(os.path.join(self.override_folder, file)):
                    shutil.copyfile(
                        os.path.join(self.override_folder, file), self.output_dir
                    )
                else:
                    try:
                        shutil.copytree(
                            os.path.join(self.override_folder, file),
                            os.path.join(self.output_dir, file),
                        )
                    except FileExistsError:
                        shutil.rmtree(os.path.join(self.output_dir, file))
                        shutil.copytree(
                            os.path.join(self.override_folder, file),
                            os.path.join(self.output_dir, file),
                        )

            self.log("Successfully extracted overrides", "info")
            mods_folder = os.path.join(self.output_dir, "mods")
            try:
                os.makedirs(mods_folder)
            except FileExistsError:
                shutil.rmtree(mods_folder)
                os.makedirs(mods_folder)

        mods_folder = self.output_dir
        self.log(f"Downloading mods to {mods_folder}", "info")
        # Adjust the progress bar(s)
        self.progressbar.setValue(0)
        self.progressbar.setMaximum(len(self.manifest))
        self.sec_progressbar.setValue(0)
        for i, mod_ in enumerate(self.manifest):
            mod = self.c.addon(mod_["projectID"])
            self.log(f"Downloading mod {i} out of {len(self.manifest)}", "info")
            self.log(f"Mod name: {mod.name}", "info")
            self.log(f"Mod url: {mod.url}", "info")
            self.log(f"Mod author(s): {str(mod.authors)}", "info")
            if mod_["required"]:
                self.log("Mod is required", "info")
                file = mod.file(mod_["fileID"])
                save_path = os.path.join(
                    mods_folder, unquote(file.download_url.split("/")[-1])
                )
                self.download_raw(file.download_url, save_path, self.sec_progressbar)
            else:
                self.log("Mod is optional", "info")
                if self.download_optional:
                    file = mod.file(mod_["fileID"])
                    save_path = os.path.join(
                        mods_folder, unquote(file.download_url.split["/"][-1])
                    )
                    self.download_raw(
                        file.download_url, save_path, self.sec_progressbar
                    )
                    self.sec_progressbar.setValue(0)
            self.step(self.progressbar, 1)
            self.secondry_log(f"{mod.name}")
        stop = now()
        self.log(
            f"Successfully installed ModPack in {str(stop - start)} seconds",
            "info",
        )

        self.clean()

    def download_raw(self, link: str, path: str, pbar: QProgressBar):
        if not self.ini:
            raise Exception("ModPack not initialized")

        r = requests.get(link, stream=True)
        with open(path, "wb") as f:
            self.log(f"LINK: {link}", "debug")
            self.log(f"PATH: {path}", "debug")
            self.log(f"HEADERS: {r.headers}", "debug")
            total_length = int(r.headers.get("content-length"))
            self.log(f"TOTAL LENGTH: {total_length}", "debug")
            for chunk in progress.bar(
                r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    self.step(pbar, 1)
        self.log(f"Downloaded {link} to %s" % path.replace("\\", "/"), "debug")

    def clean(self):
        self.log("Cleaning up...", "info")
        if self.meth == "ZIP":
            shutil.rmtree(self.tempdir, ignore_errors=True)
        self.log("Successfully cleaned up", "info")
        self.ini = False
