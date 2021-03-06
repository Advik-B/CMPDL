from cursepy import CurseClient
from tree_generator import gentree
from urllib.parse import unquote
from clint.textui import progress
from time import perf_counter as now
import zipfile
import tempfile
import os
import json
import shutil
import requests
import click
import logger


class ModPack:
    def __init__(self, path: str, **kwargs) -> None:
        self.log = kwargs.get("log_func")
        self.secondry_log = kwargs.get("secondry_log")
        # Set up the progress bar

        self.output_dir = kwargs.get("output_dir")
        self.download_optional = kwargs.get("download_optional_mods")
        self.keep_config = kwargs.get("keep_config")

        self.ini = False
        self.path = path

    def init(self):
        self.log("Initializing Curse client...", "info")
        start = now()
        self.c = CurseClient()
        stop = now()
        self.log(
            "Successfully initialized Curse client in %s seconds" % str(stop - start),
            "info",
        )
        del stop, start
        self.log("Initializing ModPack...", "info")
        start = now()
        if self.path.endswith(".zip"):
            self.tempdir = tempfile.mkdtemp(prefix="CMPDL")
            self.log("Extracting modpack to %s" % self.tempdir, "info")
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
            self.log("Manifest path set to %s" % self.manifest_path, "info")
        except AttributeError:
            self.log("Manifest path not set", "info")

        self.log("Loading manifest...", "info")
        with open(self.manifest_path, "r") as f:
            mani = json.load(f)
        self.manifest = mani["files"]
        self.log("Minecraft version: %s" % mani["minecraft"]["version"], "info")
        self.log("Modpack version: %s" % mani["version"], "info")
        self.log("Modpack name: %s" % mani["name"], "info")
        self.log("Modpack author(s): %s" % mani["author"], "info")
        self.log("Modpack description: %s" % mani.get("description"), "info")
        self.log("Modpack website: %s" % mani.get("website"), "info")
        self.log(
            "Modpack modloader: %s" % mani["minecraft"]["modLoaders"][0]["id"], "info"
        )
        self.log("Modpack config/overrides: %s" % mani["overrides"], "info")
        self.log("Successfully loaded manifest", "info")
        if self.meth == "ZIP":
            self.override_folder = os.path.join(self.tempdir, mani["overrides"])
        del mani
        stop = now()
        self.log(
            "Successfully initialized ModPack in %s seconds" % str(stop - start), "info"
        )
        del stop, start
        self.ini = True

    def install(self):
        global mods_folder
        self.log("Installing ModPack...", "info")
        start = now()
        if self.meth == "ZIP" and os.path.isdir(self.override_folder):

            self.log("Extracting overrides to %s" % self.output_dir, "info")
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
        self.log("Downloading mods to %s" % mods_folder, "info")
        # Adjust the progress bar(s)
        for i, mod_ in enumerate(self.manifest):
            mod = self.c.addon(mod_["projectID"])
            self.log("Downloading mod %s out of %s" % (i, len(self.manifest)), "info")
            self.log("Mod name: %s" % mod.name, "info")
            self.log("Mod url: %s" % mod.url, "info")
            self.log("Mod author(s): %s" % str(mod.authors), "info")
            if mod_["required"]:
                self.log("Mod is required", "info")
                file = mod.file(mod_["fileID"])
                save_path = os.path.join(
                    mods_folder, unquote(file.download_url.split("/")[-1])
                )
                self.download_raw(file.download_url, save_path)
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
            self.secondry_log("%s" % mod.name, "info")

        stop = now()
        self.log(
            "Successfully installed ModPack in %s seconds" % str(stop - start), "info"
        )
        self.clean()

    def download_raw(self, link: str, path: str):
        if not self.ini:
            raise Exception("ModPack not initialized")

        r = requests.get(link, stream=True)
        with open(path, "wb") as f:
            self.log("LINK: %s" % link, "debug")
            self.log("PATH: %s" % path, "debug")
            self.log("HEADERS: %s" % r.headers, "debug")
            total_length = int(r.headers.get("content-length"))
            self.log("TOTAL LENGTH: %s" % total_length, "debug")
            for chunk in progress.bar(
                r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
        self.log("Downloaded %s to %s" % (link, path), "debug")

    def clean(self):
        self.log("Cleaning up...", "info")
        if self.meth == "ZIP":
            shutil.rmtree(self.tempdir, ignore_errors=True)
        self.log("Successfully cleaned up", "info")
        self.ini = False


@click.command()
@click.option(
    "-o",
    "--output",
    default=os.path.join(os.path.expanduser("~"), "mods"),
    help="Output file",
)
@click.option(
    "-f",
    "--file",
    help="Input file (REQUIRED)",
    required=True,
)
@click.option("-d", "--download-optional", is_flag=True, help="Download optional mods")
@click.option(
    "-k",
    "--keep-config",
    is_flag=True,
    help="Keep config file(s) in output folder (If any)",
)
def main(output, file, download_optional, keep_config):
    global logger
    logger_ = logger.Logger()
    # Prep the kwargs
    kwargs = {
        "log_func": logger_.log,
        "secondry_log": logger_.log,
        "output_dir": output,
        "download_optional": download_optional,
        "keep_config": keep_config,
    }
    # Create the ModPack object
    try:
        m = ModPack(file, **kwargs)
        m.init()
        m.install()
    except Exception as e:
        print(e)
        print("Something went wrong, check the log for more info")
        print("If you think this is a bug, please report it on the GitHub page")
        print("https://github.com/Advik-B/CMPDL/issues/new")
        raise e
    finally:
        logger_.quit()


if __name__ == "__main__":
    main()
