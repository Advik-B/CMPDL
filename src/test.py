from v import api_key
from curseforge import CurseClient
from rich.console import Console
from requests import get
from multiprocessing import Pool
from time import perf_counter as now

import json
import os
import codecs

CLIENT = CurseClient(api_key, cache=True)

def download(url: str, chunk_size: int = 1024):

    fname = os.path.basename(url)
    fname = f"mods/{fname}"

    with get(url, stream=True) as r:
        r.raise_for_status()
        print(f"Downloading {fname}")
        count = 1
        with open(fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                print(f"Downloaded {count} chunks ({fname})")
                count += 1

        print(f"Finished downloading {fname}")

def main():
    if not os.path.exists("mods"):
        os.mkdir("mods")
    console = Console()

    with codecs.open("Sample-Modpack.json", "r", encoding="utf-8") as f:
        data = json.load(f)



    console.print("Modpack Name: " + data["name"])
    console.print("Modpack Version: " + data["version"])
    console.print("Modpack Author: " + data["author"])

    start = now() # Start timer

    mod_urls = [
        CLIENT.get_mod_file(mod["projectID"], mod["fileID"]).download_url
        for mod in data["files"]
    ]
    with Pool(8) as p:
        p.map(download, mod_urls)

    console.print("[b green]Finished downloading all mods[/]")
    stop = now() # Stop timer
    console.print(f"Time taken: {stop - start} seconds")

if __name__ == "__main__":
    main()
