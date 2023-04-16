# CMPDL (Curseforge ModPack Downloader)
> A better version of [Franckyi/CMPDL](https://github.com/Franckyi/CMPDL) rewritten in [python](https://python.org/about)

**IMPORTANT ANNOUNCEMENT :warning:** 

Due to a misssing library (A console-like GUI logs viewer). I have paused development on this project and started writing the missing library from scratch

---
[![CodeQL](https://github.com/Advik-B/CMPDL/actions/workflows/codeql.yml/badge.svg?branch=RewriteOnceMore)](https://github.com/Advik-B/CMPDL/actions/workflows/codeql.yml)
[![Python application](https://github.com/Advik-B/CMPDL/actions/workflows/python-app.yml/badge.svg?branch=RewriteOnceMore)](https://github.com/Advik-B/CMPDL/actions/workflows/python-app.yml)

---

[![img](https://img.shields.io/discord/931002932789399564?label=Discord&logo=discord&logoColor=5561f5&style=for-the-badge)](https://discord.gg/AxfhEeTJMw)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://python.org)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://pornhub.com)


## What is CMPDL

CMPDL (CurseForge Modpack Downloader) is an app that helps in downloading mods from a modpack (Not possible by a human)

If you are new to [minecraft](https://minecraft.net), you may not understand what this does. If you not ... Buddy. You Came To The Right Place 🙂

This app will download all the mods to your desired folder from a modpack (zip) file

### How it works

Every modpack is a zip file, In that zip file... there is a file called `manifest.json`

In `manifest.json` there is info about:

- Modpack Name
- What mods were used:
  - Mod Name
  - Mod ID (`project id`)
  - File ID
  - Whether it is required or not

My Program will collect the above info and generate direct download links for the mods
And it will download them one by one & save it in your dest folder

## How to build/run on **ANY** OS:

- Install python
- Download the ZipApp
- Run it with python, eg:
  ```
  python ZipApp.zip
  ```
  *or*
  ```
  python ZipApp.pyz
  python ZipApp.pyzw
  ```
