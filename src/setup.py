import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": [
        "os",
        "PyQt5",
        "threading",
        "sys",
        "clint",
        "termcolor",
        "cursepy",
        "requests",
    ],
    "excludes": [
        "tkinter",
    ],
    "include_files": [
        "assets/",
        "design.ui",
    ],
    "include_msvcr": True,
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="CMPDL",
    version="2",
    description="Cuseforge Modpack DownLoader",
    options={
        "build_exe": build_exe_options,
    },
    executables=[Executable("__main__.py", base=base, icon="assets/icon.ico")],
)
