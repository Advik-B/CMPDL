__version__ = "v2.6.0"

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTabWidget
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from sys import argv
from contextlib import suppress
from QtLogger import QtLogger
import qdarktheme
from backend.cf import *

# We need to do this to make sure that the appid is set before the window is created
# This way, windows will show the correct icon in the taskbar and in the alt-tab menu (and probably other places)
# This is only needed on Windows, so we suppress the ImportError on other platforms
with suppress(ImportError, ModuleNotFoundError):
    import ctypes

    myappid = "advik.CMPDL." + __version__.strip("v")
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
        self.setWindowIcon(QIcon("resources/icon.png"))

        self.curseforge_tab: QWidget = self.findChild(QWidget, "curseforge_tab")
        self.curseforge_view = ModDownloadList(
            API=self.curseforge_api,
            save_path=DEFAULT_SAVE_PATH,
            chunk_size=DEFAULT_CHUNK_SIZE,
        )
        self.curseforge_save_path = self.findChild(QLineEdit, "cf_output_folder_le")
        self.curseforge_start_btn = self.findChild(QPushButton, "cf_start_btn")

        # Replace the curseforge_view placeholder with the actual view
        placeholder: QWidget = self.curseforge_tab.findChild(QWidget, "cf_placeholder")
        # Get the grid position of the placeholder
        pos: tuple = self.curseforge_tab.layout().getItemPosition(self.curseforge_tab.layout().indexOf(placeholder))
        # Remove the placeholder from the layout and delete it
        self.curseforge_tab.layout().removeWidget(placeholder)
        placeholder.deleteLater()
        # Add the curseforge progress view
        self.curseforge_tab.layout().addWidget(self.curseforge_view, pos[0], pos[1])
        # Get the grid position of the log placeholder
        logger_placeholder: QWidget = self.layout().findChild(QWidget, "logger_ph")
        print(logger_placeholder)
        # Get the grid position of the placeholder
        pos: tuple = self.layout().getItemPosition(self.curseforge_tab.layout().indexOf(logger_placeholder))
        # Remove the log placeholder from the layout and delete it
        self.curseforge_tab.layout().removeWidget(logger_placeholder)
        logger_placeholder.deleteLater()
        # Add the logger
        self.logger = QtLogger()
        self.curseforge_tab.layout().addWidget(self.logger, pos[0], pos[1])
        self.curseforge_tab.layout().setColumnStretch(0, 1)
        self.curseforge_tab.layout().setColumnStretch(1, 1)
        self.curseforge_tab.layout().setRowStretch(0, 1)

        self.logger.start()
        # Connect signals

if __name__ == "__main__":
    app = QApplication(argv)
    qdarktheme.setup_theme(theme="dark")
    window = CMPDL()
    app.exec()
