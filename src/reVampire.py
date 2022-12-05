from v import api_key
import json
from curseforge.base import CurseClient
from curseforge.classes import CurseModFile

client = CurseClient(api_key=api_key, cache=True)  # type: ignore

with open("Sample-Modpack.json") as f:
    data = json.load(f)

files = data["files"]

modfiles: list[CurseModFile] = []
for _mod in files:
    modfiles.append(client.get_mod_file(_mod["projectID"], _mod["fileID"]))

for _mod in modfiles:
    print(_mod.download_url)