__version__ = "v2.6.0"

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from sys import argv
from qt_material import apply_stylesheet, list_themes
from darkdetect import isDark
from random import choice as random_choice

from .v import API_KEY

class CMPDL(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi("resources/main.ui", self)

        dark_themes = [theme for theme in list_themes() if "dark" in theme and "red" not in theme]
        light_themes = [theme for theme in list_themes() if "dark" not in theme and "red" not in theme]

        if isDark():
            apply_stylesheet(self, random_choice(dark_themes))
        else:
            apply_stylesheet(self, random_choice(light_themes))



if __name__ == "__main__":
    app = QApplication(argv)
    window = CMPDL()
    app.exec()
