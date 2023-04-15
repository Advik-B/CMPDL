# This file contains the backend for the CurseForge tab.
# It contains the ModDownloadItem and ModDownloadThread classes, which are used to download mods from CurseForge.
# It is vaguely named "cf.py" to avoid confusion with the "curseforge" module.

from curseforge import CurseClient
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QProgressBar, QListView, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from typing import Union
from requests import get
from os.path import join as path_join

class ModDownloadItem(QStandardItem):
    """
    A QStandardItem that represents a mod download.
    This class is used in ModDownloadList, and uses a ModDownloadThread to download the mod.
    """

    def __init__(self, mod_id: int, modfile_id: int, parent: QWidget):
        super().__init__()

        self.mod_id = mod_id
        self.modfile_id = modfile_id
        self.save_path = parent.save_path
        self.chunk_size = parent.chunk_size
        self.API = parent.API

        self.thread = ModDownloadThread(self)
        self.thread.finished.connect(self.finished)
        self.progress_bar = QProgressBar()
        self.mod_name = QLabel()
        self.mod_name.setText("Loading...")
        self.progress_bar.setRange(0, 0)
        self.thread.parse()


    def finished(self):
        self.progress_bar.setValue(self.progress_bar.maximum())

    def start(self):
        self.thread.start()


class ModDownloadThread(QThread):
    def __init__(self, parent: ModDownloadItem):
        super().__init__(parent)

        self.parent = parent
        self.API: CurseClient = parent.API
        self.mod_id: int = parent.mod_id
        self.modfile_id: int = parent.modfile_id

        self.progress: QProgressBar = parent.progress_bar
        self.progress.setValue(0)
        self.save_path: str = parent.save_path
        self.parent.mod_name: QLabel
        self.chunk_size: int = 4096 if parent.chunk_size is None else parent.chunk_size


        # Conditions
        self.parsed = False
        self.downloaded = False

        # Mod info
        self.file_path: str = ""
        self.download_url: str = ""
        self.file_size: int = 0


    def parse(self):
        if self.parsed:
            return

        # Set the progress bar to be indeterminate
        self.progress.setRange(0, 0)
        mod = self.API.get_mod_file(self.mod_id, self.modfile_id)
        self.file_path = path_join(self.save_path, mod.file_name)
        self.download_url = mod.download_url
        self.file_size = mod.file_length

        self.parent.mod_name.setText(mod.display_name)

        # Set the progress bar to be determinate
        self.progress.setRange(0, self.file_size)
        self.parsed = True

    def download(self):
        if self.downloaded:
            return

        self.parse()
        self.progress.setMaximum(self.file_size)
        with open(self.file_path, "wb") as f:
            response = get(self.download_url, stream=True)
            total = 0
            for data in response.iter_content(chunk_size=self.chunk_size):
                total += len(data)
                f.write(data)
                self.progress.setValue(total)
        self.downloaded = True

    run = download # Alias for download


class ModDownloadList(QListView):
    def __init__(self, API: Union[CurseClient, str], save_path: str, chunk_size: int = 2048):
        super().__init__()
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.save_path = save_path
        self.chunk_size = chunk_size

        self.testlbl = QLabel(
            "If you are seeing this\n"
            "then replacing the placeholder widget worked!",
            self
        ) # TODO: Remove this after testing


        if isinstance(API, str):
            self.API = CurseClient(API)
        elif isinstance(API, CurseClient):
            self.API = API
        else:
            raise TypeError("API must be an instance of CurseClient or a string containing the API key.")

    def add_item(self, item: QStandardItem):
        self.model.appendRow(item)

