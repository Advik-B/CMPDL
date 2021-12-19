from cursepy import CurseClient
import zipfile
import tempfile
import os
import json

class ModPack():
    
    def __init__(self, path: str) -> None:
        self.path = path
        self.ini = False
    def init(self, path: str=None) -> None:
        if path is None:
            self.outdir_temp = tempfile.mkdtemp()


        self.ini = True
        with zipfile.ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall(self.outdir_temp)
            self.modpack_files = zip_ref.namelist()

        self.manifest_path = os.path.join(self.outdir_temp, 'manifest.json')
        with open(self.manifest_path, 'r') as manifest_file:
            self.manifest = json.load(manifest_file)

        # Getting the required info
        self.modpack_name = self.manifest['name']
        self.modpack_version = self.manifest['version']
        self.modpack_authors = self.manifest['authors']
        self.mods = self.manifest['files']
        self.minecraft_version = self.manifest['minecraft']['version']
        self.modloader = self.manifest['minecraft']['modloader']
        self.overrides = self.manifest['overrides']

        

def test():
    modpack = ModPack('examples/All+the+Mods+7-0.2.6.zip')
    modpack.init()
    print(modpack.manifest)

if __name__ == '__main__':
    test()
        
# curse = CurseClient()


# addon = curse.addon(238222)
# print(addon.name)
# # print(addon.description)
# print(addon.authors[0].name)
# print(addon.download_count)
# file = addon.file(file_id=3569553)
# print(file.download_url)