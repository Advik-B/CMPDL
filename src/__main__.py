from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QLineEdit,
    QCheckBox,
    QProgressBar,
    QListWidget,
    QPushButton,
    QFileDialog,
    QTextEdit,
    )
from PyQt5 import uic
from PyQt5.QtCore import QThread
from logger import Logger
from threading import Thread
from backend import ModPack
import sys
import os

class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        # Set up the logger
        self.logger = logger

        # Load the UI
        uic.loadUi("design.ui", self)
        # Set up the window title and make it non-resizable
        self.setWindowTitle("CMPDL by Advik-B")
        self.setMaximumSize(self.size())
        # Define widgets from ui file
        self.title_lbl = self.findChild(QLabel, "title_lbl")
        self.modpack_pth = self.findChild(QLineEdit, "modpack_pth")
        self.output_dir = self.findChild(QLineEdit, "download_pth")
        self.optional_mods = self.findChild(QCheckBox, "optional_mods")
        self.keep_config = self.findChild(QCheckBox, "keep_config")
        self.overall_progress = self.findChild(QProgressBar, "progress")
        self.per_mod_progress = self.findChild(QProgressBar, "per_mod_progress")
        self.mod_list = self.findChild(QListWidget, "DownloadList")
        self.log_box = self.findChild(QTextEdit, "logbox")
        self.start_download = self.findChild(QPushButton, "start_download_btn")
        self.copy_logs = self.findChild(QPushButton, "copy_logs_btn")
        self.browse_modpack = self.findChild(QPushButton, "browse_modpack")
        self.output_dir_btn = self.findChild(QPushButton, "download_pth_browse")
        # Create a list of widgets, this is used to check if all widgets are found in the ui file and be deleted later to free up memory
        self.widgets = [

            self.title_lbl,
            self.modpack_pth,
            self.output_dir,
            self.optional_mods,
            self.keep_config,
            self.overall_progress,
            self.per_mod_progress,
            self.mod_list,
            self.log_box,
            self.start_download,
            self.copy_logs,
            self.browse_modpack,
            self.output_dir_btn,
]
        # Check if all widgets are defined properly
        # if the code below works then all widgets are defined properly
        try:
            self.log("Checking widgets", "info")
            self.check_widgets()
        except AssertionError as e:
            self.log("Widget not found: %s" % e, "error")
            sys.exit(1)
        # set up the log box
        self.log_box.setReadOnly(True)

        # Connect the buttons to their functions
        self.browse_modpack.clicked.connect(self.browse__modpack)
        self.output_dir_btn.clicked.connect(self.browse_output_dir)
        self.copy_logs.clicked.connect(self.copy_logs_func)
        self.start_download.clicked.connect(self.start_payload)
        # show the window
        self.show()
        self.log("Window sucessfully loaded", "info")

    def log(self, message: str, type_: str):

        msg = self.logger.log(message, type_)
        try:

            self.log_box.setReadOnly(False)
            self.log_box.setText(self.log_box.toPlainText() + str(msg)+ '\n')
            self.log_box.setReadOnly(True)
        except AttributeError:
            self.logger.log("Log box not found", "error")

    def check_widgets(self):
        for widget in self.widgets:
            self.log(widget, "debug")
            assert widget is not None, "Widget not found"
        # Free up memory by deleting the list
        del self.widgets

    def browse__modpack(self):
        """Browse for a .json / .zip file"""
        file_ = QFileDialog.getOpenFileName(
            self,
            caption="Select modpack or a manifest file",
            filter="Manifest (*.json);;ModPack (*.zip)",
            initialFilter="ModPack (*.zip)",
            directory=os.path.expanduser("~"),
            )

        if file_[0]:
            self.modpack_pth.setText(file_[0])
            self.log("Modpack path set to: %s" % file_[0], "info")

    def browse_output_dir(self):
        """Browse for a directory"""
        if directory := QFileDialog.getExistingDirectory(
            self,
            caption="Select output directory",
        ):
            self.output_dir.setText(directory)
            self.log("Output directory set to: %s" % directory, "info")

    def copy_logs_func(self):
        """Copy the logs to the clipboard"""
        self.log_box.selectAll()
        self.log_box.copy()
        self.log_box.undo()
        self.log("Logs copied to clipboard", "info")

    def secondry_log(self, message: str):
        """Secondry log function"""
        self.log(message, "info")
        self.mod_list.addItem(message)

    def start_payload(self):
        try:
            kwargs = {

                'log_func': self.log,
                'secondry_log': self.secondry_log,
                'pbar': self.overall_progress,
                'pbar2': self.per_mod_progress,
                'output_dir': self.output_dir.text(),
                'download_optional_mods': self.optional_mods.isChecked(),
                'keep_config': self.keep_config.isChecked(),

            }

            self.log("Starting payload", "info")
            modpack = ModPack(self.modpack_pth.text(), **kwargs)
            modpack.init()
            t = Thread(target=modpack.install)
            t.start()

        except Exception as e:
            self.log('Error: %s' % e, 'error')
            self.log("Payload failed", "error")
            raise e
            # Disable this ^^ in a production environment
            # Enable this ^^ in debug mode
        return

def main():
    global logger
    logger = Logger()
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.setActiveWindow(UIWindow)
    app.exec_()
    logger.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
