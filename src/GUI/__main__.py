__version__ = "v2.6.0"

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from sys import argv
from contextlib import suppress
import qdarktheme
from backend.cf import *


# We need to do this to make sure that the appid is set before the window is created
# This way, windows will show the correct icon in the taskbar and in the alt-tab menu (and probably other places)
# This is only needed on Windows, so we suppress the ImportError on other platforms
with suppress(ImportError, ModuleNotFoundError):
    import ctypes
    myappid = "advik.CMPDL."  + __version__.strip("v")
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from .v import API_KEY

# Constants
DEFAULT_CHUNK_SIZE = 2048
DEFAULT_SAVE_PATH = "CMPDL_Mods"



class CMPDL(QWidget):
    def __init__(self):
        super().__init__()
        self.curseforge_tab = None
        self.curseforge_api = CurseClient(API_KEY)
        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi("resources/interface.ui", self)
        # Set window icon

        self.curseforge_tab: QWidget = self.findChild(QWidget, "curseforge_tab")
        self.curseforge_view = ModDownloadList(
            API=self.curseforge_api,
            save_path=DEFAULT_SAVE_PATH,
            chunk_size=DEFAULT_CHUNK_SIZE,
        )
        self.curseforge_save_path = self.findChild(QLineEdit, "cf_output_folder_le")
        self.curseforge_start_btn = self.findChild(QPushButton, "cf_start_btn")
        # Replace the placeholder widget with the actual widget
        # Find the placeholder widget
        placeholder: QWidget = self.curseforge_tab.findChild(QWidget, "cf_placeholder")
        # Get the placeholder widget's x and y grid positions
        x = self.curseforge_tab.layout().getItemPosition(self.curseforge_tab.layout().indexOf(placeholder))
        # Remove the placeholder widget
        self.curseforge_tab.layout().removeWidget(placeholder)
        # Add the actual widget
        self.curseforge_tab.layout().addWidget(self.curseforge_view, x[0], x[1])
        self.setWindowIcon(QIcon("resources/icon.png"))



if __name__ == "__main__":
    app = QApplication(argv)
    qdarktheme.setup_theme(theme="dark")
    window = CMPDL()
    app.exec()
