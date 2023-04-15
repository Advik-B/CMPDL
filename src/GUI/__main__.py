__version__ = "v2.6.0"

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from sys import argv
from contextlib import suppress
import qdarktheme


# We need to do this to make sure that the appid is set before the window is created
# This way, windows will show the correct icon in the taskbar and in the alt-tab menu (and probably other places)
# This is only needed on Windows, so we suppress the ImportError on other platforms
with suppress(ImportError, ModuleNotFoundError):
    import ctypes
    myappid = "advik.CMPDL."  + __version__.strip("v")
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from .v import API_KEY


class CMPDL(QWidget):
    def __init__(self):
        super().__init__()
        self.st: str = ""

        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi("resources/interface.ui", self)
        # Set window icon
        self.setWindowIcon(QIcon("resources/icon.png"))



if __name__ == "__main__":
    app = QApplication(argv)
    qdarktheme.setup_theme(theme="dark")
    window = CMPDL()
    app.exec()
