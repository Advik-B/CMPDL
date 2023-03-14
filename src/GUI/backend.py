from curseforge import CurseClient
from curseforge.classes import CurseModFile
from .v import api_key
from PyQt6.QtWidgets import QWidget, QProgressBar, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
from requests import get

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    def __init__(self, parent: QWidget, client: CurseClient, project_id: int, file_id: int, folder_name: str):
        super().__init__(parent)
        self.client = client
        self.project_id = project_id
        self.file_id = file_id
        self.folder_name = folder_name
        self.progress.connect(parent.update_progress)
    def run(self):
        mod: CurseModFile = self.client.get_mod_file(self.project_id, self.file_id)
        download_url: str = mod.download_url
        file_name: str = mod.file_name
        display_name: str = mod.display_name
        file_size: int = mod.file_length

        r = get(download_url, stream=True)
        with open(f"{self.folder_name}/{file_name}", "wb") as mod_file:
            # Download the mod while updating the progress bar
            downloaded = 0
            for chunk in r.iter_content(chunk_size=1024):
                pass
