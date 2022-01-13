from cursepy import CurseClient
from logger import Logger
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
        if type(kwargs) == dict and len(kwargs) > 0:
            self.log = kwargs.get("log_func")
            self.secondry_log = kwargs.get("secondry_log")
            # Set up the progress bar
            self.progressbar = kwargs.get("pbar")
            self.progressbar.setValue(0)
            self.progressbar.setMaximum(100)
            
            self.sec_progressbar = QProgressBar(kwargs.get("pbar2"))
            self.output_dir = kwargs.get("output_dir")
            self.download_optional = kwargs.get("download_optional_mods")
            self.keep_config = kwargs.get("keep_config")
        
        else:
            logger = Logger()
            self.log = logger.log
            self.secondry_log = logger.log
            
            self.progressbar = QProgressBar()
            self.sec_progressbar = self.progressbar
            self.output_dir = "."
        
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
            
            
        self.ini = True