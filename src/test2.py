from v import api_key
from curseforge import CurseClient
from rich.console import Console
from rich.progress import Progress
from multiprocessing import Pool
from time import perf_counter as now # Benchmarking
from requests import get

import json
import os

