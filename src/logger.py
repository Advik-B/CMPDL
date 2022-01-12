# This is the logger module. (Not in pypi)

import datetime
from termcolor import colored


class Logger:
    def __init__(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        self.log_file = 'logs/' + date

    def log(self, message, type_):
        # Get the current time with milliseconds
        # time = datetime.datetime.now().strftime('%H:%M:%S:%f')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        # format_ = f'[{time}]-[{type_.upper()}]: {message}'
        types = {

            "info": 'green',
            "warning": 'yellow',
            "error": 'red',
            "debug": 'cyan'
        }
        format_ = f'[{colored(time, "yellow")}]-\
[{colored(type_.upper(), types[type_])}]:\
{colored(message, "white")}'
        print(format_)
