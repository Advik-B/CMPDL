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
from tkinter.ttk import Progressbar
from urllib.parse import quote, unquote
from logger import Logger

logger = Logger()
logger.init(telemetry=True)

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
        logger.log('info', 'Initializing ModPack')
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
            logger.log('error', 'ModPack not initialized')
            raise ModPackError('ModPack not initialized')
        return self.base_url.replace('<id>', str(project_id)).replace('<file>', str(file_id))

    def get_links(self):
        if self.ini == False:
            logger.log('error', 'ModPack not initialized')
            raise ModPackError('ModPack not initialized')
        logger.log('info', 'Getting links')
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
        logger.log('info', 'Links gotten')
        return self.links

    def clean(self):
        logger.log('info', 'Cleaning up')
        shutil.rmtree(self.tempfol, ignore_errors=True)
        self.ini = False
        self.gotten_links = False
        logger.log('info', 'Cleanup complete')

    def install(self, path:str, progress_bar:Progressbar=None):
        logger.log('info', 'Installing in %s' % path)
        if self.ini is False:
            logger.log('error', 'ModPack not initialized')
            raise ModPackError('ModPack not initialized')
        elif self.gotten_links is False:
            logger.log('error', 'Links not gotten')
            raise ModPackError('Links not gotten')
        scraper = cloudscraper.create_scraper(allow_brotli=True)
        re_ = r'href="/minecraft/mc-mods/.+\/files"'
        total_file = len(self.links)
        if progress_bar is not None:
            progress_bar.config(maximum=total_file)
        logger.log('info', 'Total files: %s' % total_file)
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
            
            r= scraper.get(new_download_link, allow_redirects=True, stream=True)
            pth = os.path.join(path, unquote(file_name))
            with open(pth, 'wb') as f:
                    total_length = int(r.headers.get('content-length', 0))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
            logger.log('info', 'Installed %s' % mod_name)
            logger.log('info', 'File path: %s' % pth)
            logger.log('info', 'File size: %s' % total_length)
            logger.log('info', 'Download link: %s' % new_download_link)
            logger.log('debug', '-----------------------------------------------------')
            if progress_bar is not None:
                progress_bar.step(1)

if __name__ == '__main__':
    a = ModPack('fab.zip')
    a.init()
    a.get_links()
    a.install('mods')
    a.clean()
