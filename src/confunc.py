#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
from tkinter.ttk import Progressbar
cwd = os.getcwd()
def download_modpack(url:str,):
    from clint.textui import progress
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'}
    r = requests.get(url, stream=True ,headers=None)
    path = os.path.join(cwd, 'mod.pack.zip')
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length', 0))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

def download_modpack_Tk_ST(url:str, bar:Progressbar):
    from clint.textui import progress
    r = requests.get(url, stream=True)
    
    path = os.path.join(cwd , 'mod.pack.zip')
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length', 0))
        bar.config(maximum=total_length)
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
                bar.step(1024)

def download_modpack_Tk(url:str, bar:Progressbar):
    from threading import Thread
    t = Thread(target=lambda: download_modpack_Tk_ST(url, bar))
    t.start()
