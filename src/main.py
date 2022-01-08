
figlet = r'''
  _____               __  __           _ _____           _    _____                      _                 _           
 / ____|             |  \/  |         | |  __ \         | |  |  __ \                    | |               | |          
| |    _   _ ___  ___| \  / | ___   __| | |__) |_ _  ___| | _| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
| |   | | | / __|/ _ \ |\/| |/ _ \ / _` |  ___/ _` |/ __| |/ / |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |___| |_| \__ \  __/ |  | | (_) | (_| | |  | (_| | (__|   <| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 \_____\__,_|___/\___|_|  |_|\___/ \__,_|_|   \__,_|\___|_|\_\_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|

______           ___       _         _  _            ______ 
| ___ \         / _ \     | |       (_)| |           | ___ \
| |_/ / _   _  / /_\ \  __| |__   __ _ | | __ ______ | |_/ /
| ___ \| | | | |  _  | / _` |\ \ / /| || |/ /|______|| ___ \
| |_/ /| |_| | | | | || (_| | \ V / | ||   <         | |_/ /
\____/  \__, | \_| |_/ \__,_|  \_/  |_||_|\_\        \____/ 
         __/ |                                              
        |___/ 

'''

import argparse
import os
from builtins import exit
from termcolor import cprint, colored
from itertools import cycle
from index import ModPack

def banner():
    clrs = cycle(['blue', 'cyan', 'green', 'yellow', 'red', 'magenta'])
    for line in figlet.splitlines():
        cprint(line, next(clrs))

parser = argparse.ArgumentParser(description='Download mods from a zip file')
parser.add_argument('-f', '--file', type=str, help='The zip file to extract', required=True)
parser.add_argument('-o', '--output', type=str, help='The output directory', required=False)
group = parser.add_mutually_exclusive_group()
group.add_argument('-s ', '--silent', action='store_true', help='Silent mode')
group.add_argument('-d', '--debug', action='store_true', help='Show debug messages')

args  = parser.parse_args()

silent = args.silent
output_dir = args.output
zip_file = args.file
debug = args.debug

if output_dir is None and zip_file is None:
    output_dir = os.path.join(os.getcwd(), 'mods')
    mode = 'gui'
elif output_dir is None or output_dir.replace(' ', '') == '':
    output_dir = os.path.join(os.getcwd(), 'mods')
    mode = 'cli'
elif zip_file is None:
    parser.error('You must specify a zip file')
    exit(1)
else:
    mode = 'cli'
def log(msg: str, level: str, silent:bool=silent, debug:bool=debug):
    if silent:
        return
    
    level = level.casefold()
    levels = {
            'info':'green',
            'error':'red', 
            'debug':'cyan', 
            'warning':'yellow'
            }

    if level not in levels:
        parser.error('Invalid log level')

    message = colored(msg, 'white')
    if debug:
        prefix = colored(f'[ {level.upper()} ]', levels[level])
        print(f'{prefix}: {message}')
    else:
        print(f'{message}')
    return

def cli(silent:bool, debug:bool, file_: str, output_dir: str):
    if not os.path.isdir(output_dir):
        log('The directory %s does not exist.' % output_dir, 'warning', silent, debug)
        log('Creating directory %s' % output_dir, 'info', silent, debug)
        try:
            os.makedirs(output_dir)
            log('Directory %s created' % output_dir, 'info', silent, debug)
        except Exception as e:
            log(f'Failed to create directory {output_dir} because of the following error:\t\n{e}', 'error', silent, debug)
            exit(1)
    if os.path.isfile(file_):
        modpack = ModPack(file_, log)
        modpack.init()
        modpack.get_links()
        modpack.install(output_dir)

if mode == 'cli':
    cli(silent, debug, zip_file, output_dir)
    banner()