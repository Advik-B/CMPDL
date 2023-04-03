from curseforge import CurseClient
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QProgressBar, QListView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from typing import Union


class ModDownloadList(QListView):
    def __init__(self, parent: QWidget = None, API: Union[CurseClient, str] = None):
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
