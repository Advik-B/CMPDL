from curseforge import CurseClient
from PyQt6.QtWidgets import QWidget, QProgressBar, QGridLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from requests import get
from os.path import join as pjoin
from .v import api_key

client = CurseClient(api_key, cache=True)

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    def __init__(self, parent, project_id: int, file_id: int, save_path: str, chunk_size: int = 1024):
        super().__init__(parent)
        self.project_id = project_id
        self.file_id = file_id
        self.save_path = save_path
        self.chunk_size = chunk_size

    def run(self):
        mod_file = client.get_mod_file(self.project_id, self.file_id)
        file_size = mod_file.file_length
        write_path = pjoin(self.save_path, mod_file.file_name)
        print(f"Downloading {mod_file.file_name} to {write_path}..."
              f"({file_size} bytes)")

        print(f"Download URL: {mod_file.download_url}")
        with open(write_path, "wb") as f:
            response = get(mod_file.download_url, stream=True)
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                f.write(chunk)
                self.progress.emit(f.tell() / file_size * 100)

class DownloadWidget(QWidget):
    def __init__(self, parent, project_id: int, file_id: int, save_path: str):
        super().__init__(parent)
        self.project_id = project_id
        self.file_id = file_id
        self.save_path = save_path
        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.progress_bar, 0, 0, 1, 2)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel)
        self.layout.addWidget(self.cancel_button, 1, 0)
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start)
        self.layout.addWidget(self.start_button, 1, 1)
        self.setLayout(self.layout)

    def start(self):
        self.thread = DownloadThread(self, self.project_id, self.file_id, self.save_path)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.start()

    def cancel(self):
        self.thread.terminate()
        self.thread.wait()
