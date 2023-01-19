from v import api_key
from curseforge import CurseClient
from typing import Optional
class BaseModPack: pass

class CurseForgeModPack(BaseModPack):
    def __init__(
            self,
            file_path: str,
            client: CurseClient,
            download_only_required: bool = True,
            on_download: Optional[callable] = lambda file_id, mod_id, json: None,
    ):
        self.file_path = file_path
        self.client = client
        self.dl_only_req = download_only_required
        self.on_download = on_download

