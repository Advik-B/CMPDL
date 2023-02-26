from .backend import client, DownloadWidget
from PyQt6.QtWidgets import QApplication


# from PyQt6.uic import loadUi
# from PyQt6.QtWidgets import QApplication, QWidget
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         loadUi("GUI/form.ui", self)
#         self.setup_ui()
#
#     def setup_ui(self):
#         self.show()
#
#
# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainWindow()
#     app.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = DownloadWidget(None, 319596, 3457597, ".")
    window.show()
    app.exec()