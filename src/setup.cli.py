from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": [
        "os",
        'cursepy',
        'urllib',
        'clint',
        'time',
        'zipfile',
        'tempfile',
        'json',
        'shutil',
        'requests',
        'click',
        'datetime',
        'termcolor',
            
        ],
    "excludes": [
        
        'tkinter',
        'PyQt5',
    ],

    "include_msvcr": True,
    
}

# base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name = "CMPDL",
    version = "1.5",
    description = "Cuseforge Modpack DownLoader",
    options = {"build_exe": build_exe_options,},
    executables = [
        Executable(
            "cli.py",
            # base=base,
            icon='assets/icon.ico'
            )
        ]
    )
