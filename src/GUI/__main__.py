__version__ = "v2.6.0"

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from sys import argv

class CMPDL(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show()

    def setupUI(self):
        loadUi("resources/main.ui", self)



if __name__ == "__main__":
    app = QApplication(argv)
    window = CMPDL()
    app.exec()