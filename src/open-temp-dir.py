from tempfile import gettempdir
from platform import system
import os

sys = system()
if sys == "Windows":
    os.startfile(gettempdir())  # type: ignore
elif sys == "Linux":
    os.system("xdg-open " + gettempdir())
elif sys == "Darwin":
    os.system("open " + gettempdir())