__version__ = "v2.6.0"

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from sys import argv
from qt_material import apply_stylesheet, list_themes
from darkdetect import isDark
from random import choice as random_choice
from contextlib import suppress
from os import system

# We need to do this to make sure that the appid is set before the window is created
# This way, windows will show the correct icon in the taskbar and in the alt-tab menu
with suppress(ImportError, ModuleNotFoundError):
    import ctypes
    myappid = "advik.CMPDL."  + __version__.strip("v")
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



from .v import API_KEY

DISALLOWED_COLOURS = ["red", "magenta"]
dark_themes = []
light_themes = []

for theme in list_themes():
    if any(colour in theme for colour in DISALLOWED_COLOURS):
        continue
    if "dark" in theme:
        dark_themes.append(theme)
    else:
        light_themes.append(theme)

class CMPDL(QWidget):
    def __init__(self):
        super().__init__()
        self.st: str = ""

        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi("resources/main.ui", self)
        # Set window icon
        self.setWindowIcon(QIcon("resources/icon.png"))
        self.theme()


    def theme(self):

        if isDark():
            self.st = random_choice(dark_themes)

        else:
            self.st = random_choice(light_themes)

        apply_stylesheet(self, self.st)



if __name__ == "__main__":
    app = QApplication(argv)
    window = CMPDL()
    app.exec()
