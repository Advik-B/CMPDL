from curseforge import CurseClient
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QProgressBar, QListView, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from typing import Union
from requests import get
from urllib3.exceptions import InsecureRequestWarning
from warnings import simplefilter
from os.path import join as path_join

class ModDownloadThread(QThread):
    def __init__(self, parent: QWidget):
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


class ModDownloadItem(QStandardItem):
    """
    A QStandardItem that represents a mod download.
    This class is used in ModDownloadList, and uses a ModDownloadThread to download the mod.
    """

    def __init__(self, mod_id: int, modfile_id: int, save_path: str, chunk_size: int = None):
        super().__init__()

        self.mod_id = mod_id
        self.modfile_id = modfile_id
        self.save_path = save_path
        self.chunk_size = chunk_size

        self.thread = ModDownloadThread(self)



class ModDownloadList(QListView):
    def __init__(self, parent: QWidget, API: Union[CurseClient, str]):
        super().__init__(parent)

        self.model = QStandardItemModel()
        self.setModel(self.model)

        if isinstance(API, str):
            self.API = CurseClient(API)
        elif isinstance(API, CurseClient):
            self.API = API
        else:
            raise TypeError("API must be an instance of CurseClient or a string containing the API key.")

    def add_item(self, item: QStandardItem):
        self.model.appendRow(item)
