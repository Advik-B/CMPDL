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
        self.keep_config = keep_files
        self.path = path
        self.output_dir = output_dir
        self.optional_mod = download_optional_mods


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
        pass