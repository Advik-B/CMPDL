#!bin/env python3

import json
import os
import tempfile
import shutil
import cloudscraper
import re
from zipfile import ZipFile
from bs4 import BeautifulSoup
from clint.textui import progress

class ModPackError(Exception): pass

class ModPack():
    def __init__(self, path) -> None:
        self.files = []
        self.links = []
        self.path_to_mods = path
        self.base_url = 'https://minecraft.curseforge.com/projects/<id>/files/<file>/download'
        self.tempfol = os.path.join(tempfile.gettempdir(), 'mc.modpack.python').replace('\\', '/')
        self.ini = False
        self.mani = os.path.join(self.tempfol, 'manifest.json').replace('\\', '/')
        self.gotten_links = False

    def init(self):
        os.makedirs(self.tempfol, exist_ok=True)
        with ZipFile(self.path_to_mods, 'r') as zip_:
            zip_.extractall(self.tempfol)
            self.lst = zip_.namelist()

        for file_ in self.lst:
            nm = os.path.join(self.tempfol, file_).replace('\\', '/')
            self.files.append(nm)
        self.ini = True

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
        shutil.rmtree(self.tempfol, ignore_errors=True)
        self.ini = False
        self.gotten_links = False

    def install(self, path:str):
        if self.ini == False:
            raise ModPackError('ModPack not initialized')
        elif self.gotten_links == False:
            raise ModPackError('Links not gotten')
        scraper = cloudscraper.create_scraper(allow_brotli=True)
        for i in range(1+1):
            html = scraper.get(self.links[i]).text
            soup = BeautifulSoup(html, 'html.parser')
            re_ = r'href="/minecraft/mc-mods/.+\/files"'
            file_link = 'https://curseforge.com'+re.findall(re_, html)[0].replace('href=', '').replace('"', '').replace("'", '')
            
            mod_name = file_link.split('/')[-2]
            file_id = self.links[i].split('/')[-2]
            download_link = 'https://www.curseforge.com/minecraft/mc-mods/%s/download/%s' % (mod_name, file_id)
            scraper_ = cloudscraper.create_scraper(delay=6)
            r= scraper_.get(download_link, allow_redirects=True, stream=True)
            pth = os.path.join(path, mod_name+'.jar')
            with open(pth, 'wb') as f:
                    total_length = int(r.headers.get('content-length', 0))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
            print('%s installed' % mod_name)
        
        
if __name__ == '__main__':
    a = ModPack('E:/GitHub-Repos/CMPDL/src/mods.zip')
    a.init()
    a.get_links()
    a.install('E:/GitHub-Repos/CMPDL/src/mods')
    a.clean()
    