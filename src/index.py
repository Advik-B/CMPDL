#!bin/env python3

if __name__ == '__main__':
    raise ImportError('This module is not meant to be run directly.')

import json
import os
import tempfile
import shutil
import cloudscraper
import re

from zipfile import ZipFile
from bs4 import BeautifulSoup
from clint.textui import progress
from tkinter.ttk import Progressbar
from urllib.parse import quote, unquote

class ModPackError(Exception): pass

class ModPack():
    
    def __init__(self, path, func) -> None:
        self.files = []
        self.links = []
        self.path_to_mods = path
        self.base_url = 'https://minecraft.curseforge.com/projects/<id>/files/<file>/download'
        self.tempfol = os.path.join(tempfile.gettempdir(), 'mc.modpack.python').replace('\\', '/')
        self.ini = False
        self.mani = os.path.join(self.tempfol, 'manifest.json').replace('\\', '/')
        self.gotten_links = False
        self.func = func

    def init(self):
        self.func('Initializing ModPack', 'info')
        os.makedirs(self.tempfol, exist_ok=True)
        with ZipFile(self.path_to_mods, 'r') as zip_:
            zip_.extractall(self.tempfol)
            self.lst = zip_.namelist()
            msg = ''.join(line + '\n' for line in self.lst)
            self.func(f'Files in modPack:\n{msg}', 'debug')

        for file_ in self.lst:
            nm = os.path.join(self.tempfol, file_).replace('\\', '/')
            self.files.append(nm)
        self.ini = True
        self.func('Initialized ModPack', 'info')

    def __get_link(self, project_id:int, file_id:int) -> str:
        if self.ini == False:
            raise ModPackError('ModPack not initialized')
        return self.base_url.replace('<id>', str(project_id)).replace('<file>', str(file_id))

    def get_links(self):
        if self.ini == False:
            raise ModPackError('ModPack not initialized')
        with open(self.mani, 'r') as f:
            mainfest = f.read()

        mainfest_dict = json.loads(mainfest)
        mainfest_files = mainfest_dict['files']
        
        for file_ in mainfest_files:
            project_id = file_['projectID']
            file_id = file_['fileID']
            url = self.__get_link(project_id, file_id)
            self.links.append(url)
        self.gotten_links = True
        return self.links

    def clean(self):
        self.func('Cleaning up unnessory files...', 'info')
        shutil.rmtree(self.tempfol, ignore_errors=True)
        self.ini = False
        self.gotten_links = False

    def install(self, path:str, progress_bar:Progressbar=None):
        if self.ini is False:
            raise ModPackError('ModPack not initialized')
        elif self.gotten_links is False:
            raise ModPackError('Links not gotten')
        scraper = cloudscraper.create_scraper(allow_brotli=True)
        re_ = r'href="/minecraft/mc-mods/.+\/files"'
        if progress_bar is not None:
            total_file = len(self.links)
            progress_bar.config(maximum=total_file)
        for i in self.links:
            html = scraper.get(i).text
            file_link = 'https://curseforge.com'+re.findall(re_, html)[0].replace('href=', '').replace('"', '').replace("'", '')
            mod_name = file_link.split('/')[-2]
            file_id = i.split('/')[-2]
            accurate_file_link = file_link.__add__('/' + str(file_id))
            a = scraper.get(accurate_file_link)
            soup = BeautifulSoup(a.text, 'html.parser')
            file_name = quote(soup.find_all(class_='text-sm')[3].text)
            file_prefix = file_id[4:]
            if file_prefix.startswith('0'):
                file_prefix = file_prefix[1:]

            new_download_link = 'https://media.forgecdn.net/files/%s/%s/%s' % (file_id[:4], file_prefix, file_name)
            project_id = i.split('/')[-4]
            msh = "\n\tMod name: %s\n\tFile name: %s\n\tLink: %s\n\tDirect download link: %s\n\tProject Id: %s\n\t"
            self.func('Getting mod with the following details:', 'info')
            self.func(msh % (mod_name, unquote(file_name), file_link, new_download_link, project_id), 'info')
            r= scraper.get(new_download_link, allow_redirects=True, stream=True)
            pth = os.path.join(path, unquote(file_name))
            with open(pth, 'wb') as f:
                    total_length = int(r.headers.get('content-length', 0))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
            if progress_bar is not None:
                progress_bar.step(1)
            self.func('Downloaded Mod: %s' % mod_name, 'info')
        self.func('All mods downloaded', 'info')
        self.clean()
        self.func('===== Done =====', 'info')
