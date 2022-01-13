from cursepy import CurseClient
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
        
    @staticmethod
    def step(pbar: QProgressBar, value: int):
        pbar.setValue(pbar.value() + value)

    def init(self):
        self.log("Initializing Curse client...", 'info')
        start = now()
        self.c = CurseClient()
        stop = now()
        self.log("Successfully initialized Curse client in %s seconds" % stop - start,
                 'info')
        del stop, start
        self.log("Initializing ModPack...", 'info')
        start = now()
        if self.path.endswith('.zip'):
            self.tempdir = tempfile.mkdtemp(prefix='CMPDL')
            self.log("Extracting modpack to %s" % self.tempdir, 'info')
            with zipfile.ZipFile(self.path, 'r') as z:
                z.extractall(self.tempdir)
            self.log("Successfully extracted modpack", 'info')
            self.log("ModPack file structure:\n%s" % gentree(self.tempdir), 'info')
            self.manifest_path = os.path.join(self.tempdir, 'manifest.json')
            self.meth = 'ZIP'
        elif self.path.endswith('.json'):
            self.manifest_path = self.path
            self.meth = 'JSON'
        
        self.log("Manifest path set to %s" % self.manifest_path, 'info')
        self.log("Loading manifest...", 'info')
        with open(self.manifest_path, 'r') as f:
            mani = json.load(f)
        self.manifest = mani['files']
        self.log("Minecraft version: %s" % mani['minecraft']['version'], 'info')
        self.log("Modpack version: %s" % mani['version'], 'info')
        self.log("Modpack name: %s" % mani['name'], 'info')
        self.log("Modpack author(s): %s" % mani['author'], 'info')
        self.log("Modpack description: %s" % mani.get('description'), 'info')
        self.log("Modpack website: %s" % mani.get('website'), 'info')
        self.log("Modpack modloader: %s" % mani['minecraft']["modLoaders"][0]['id'], 'info')
        self.log("Modpack config/overrides: %s" % mani['overrides'], 'info')
        self.log("Successfully loaded manifest", 'info')
        if self.meth == 'ZIP':
            self.override_folder = os.path.join(self.tempdir, mani['overrides'])
        del mani
        stop = now()
        self.log("Successfully initialized ModPack in %s seconds" % stop - start)
        del stop, start
        self.ini = True
    
    def install(self):
        pass
    
    def download_raw(self, link: str, path: str, pbar: QProgressBar):
        if not self.ini:
            raise Exception("ModPack not initialized")

        r = requests.get(link, stream=True)
        with open(path, 'wb') as f:
            self.log('LINK: %s' % link, 'debug')
            self.log('PATH: %s' % path, 'debug')
            self.log('HEADERS: %s' % r.headers, 'debug')
            total_length = int(r.headers.get('content-length'))
            self.log('TOTAL LENGTH: %s' % total_length, 'debug')
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    self.step(pbar, 1)
        self.log('Downloaded %s to %s' % (link, path), 'debug')
