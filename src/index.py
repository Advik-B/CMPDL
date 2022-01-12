from cursepy import CurseClient
from logger import Logger
from tree_generator import gentree
from urllib.parse import unquote
from clint.textui import progress
from tkinter.ttk import Progressbar
import zipfile
import tempfile
import os
import json
import shutil
import requests


class ModPack:

    def __init__(self, path: str, loggerfunc=None) -> None:
        self.path = path
        self.ini = False
        self.logger = Logger()
        self.log = self.logger.log
        if loggerfunc is not None:
            self.log = loggerfunc

    def init(self, path: str = None) -> None:
        if path is None:
            self.outdir_temp = tempfile.mkdtemp(prefix='CMPDL')

        with zipfile.ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall(self.outdir_temp)
            self.modpack_files = zip_ref.namelist()

        self.manifest_path = os.path.join(self.outdir_temp, 'manifest.json')
        with open(self.manifest_path, 'r') as manifest_file:
            self.manifest = json.load(manifest_file)

        # Getting the required info
        self.modpack_name = self.manifest['name']
        self.modpack_version = self.manifest['version']
        self.modpack_authors = self.manifest['author']
        self.mods = self.manifest['files']
        self.minecraft_version = self.manifest['minecraft']['version']
        self.modloader = self.manifest['minecraft']['modLoaders']
        for mod in self.modloader:
            if mod.get('primary') is True:
                self.modloader = mod['id']
                break

        self.overrides = self.manifest['overrides']
        self.log(f'Modpack: {self.modpack_name}', 'info')
        self.log(f'Version: {self.modpack_version}', 'info')
        self.log(f'Authors: {self.modpack_authors}', 'info')
        self.log(f'Minecraft version: {self.minecraft_version}', 'info')
        self.log(f'Modloader: {self.modloader}', 'info')
        self.log(f'Overrides Folder: {self.overrides}', 'debug')
        temp_msg = 'Files in modpack:\n%s' % gentree(self.outdir_temp)
        self.log(temp_msg, 'info')
        self.client = CurseClient()
        del temp_msg
        self.ini = True

    def download_mods(self, output_dir: str, pbar: Progressbar) -> None:
        pbar.config(maximum=len(self.mods))
        for mod in self.mods:
            self.current_mod = self.client.addon(mod['projectID'])
            self.log(f'Downloading {self.current_mod.name}', 'info')
            self.log(f'Mod ProjectID: {mod["projectID"]}', 'debug')
            self.log(f'Mod FileID: {mod["fileID"]}', 'debug')
            self.download_raw(
                self.current_mod.file(
                    mod["fileID"]).download_url,
                output_dir)
            self.log(f'Downloaded {self.current_mod.name} complete', 'info')
            pbar.step(1)

    def download_raw(self, url: str, output_dir: str) -> None:
        r = requests.get(url, stream=True)
        file_name = unquote(url.split('/')[-1])
        output_path = os.path.join(output_dir, file_name)
        with open(output_path, 'wb') as f:
            for chunk in progress.bar(
                    r.iter_content(chunk_size=1024),
                    expected_size=(int(r.headers['content-length']) / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        del r

    def clean(self):
        if self.ini:
            self.log('Cleaning up', 'info')
            shutil.rmtree(self.outdir_temp, ignore_errors=True)
            self.ini = False
            self.log('Cleanup complete', 'info')


def test():
    # r = requests.get('https://media.forgecdn.net/files/3571/571/All+the+Mods+7-0.2.6.zip')
    # with open('All+the+Mods+7-0.2.6.zip', 'wb') as f:
    #     f.write(r.content)
    modpack = ModPack('examples/All+the+Mods+7-0.2.6.zip')
    modpack.init()
    modpack.download_mods(r'E:\GitHub-Repos\CMPDL\src\downloads')
    modpack.clean()


if __name__ == '__main__':
    test()

# addon = curse.addon(238222)
# print(addon.name)
# # print(addon.description)
# print(addon.authors[0].name)
# print(addon.download_count)
# file = addon.file(file_id=3569553)
# print(file.download_url)
