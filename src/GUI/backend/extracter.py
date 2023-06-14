import zipfile
import json
import os
import shutil
from curseforge import CurseClient
from curseforge.classes import CurseModFileManifest
from typing import Union

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QProgressBar, QListView, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class Modpack:

    def __init__(self,
                 path: str,
                 logger: