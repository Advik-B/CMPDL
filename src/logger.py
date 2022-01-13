# This is the logger module. (Not in pypi)

import datetime
import os
from termcolor import colored

class Logger:
    def __init__(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        self.log_file_name = 'logs/' + date
        if os.path.isfile('logs'):
            try:
                os.remove('logs')
                os.mkdir('logs')
            except [OSError, PermissionError]:
                print("[ERROR] Unable to create logs directory")
        elif os.path.isdir('logs'):
            pass
        else:
            os.mkdir('logs')
        self.log_file = open(self.log_file_name, 'a')

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
[{colored(type_.upper(), types[type_])}]: \
{colored(message, "white")}'
        file_format = f'[{time}]-[{type_.upper()}]: {message}\n'
        print(format_)
        self.log_file.write(file_format)
        del format_, file_format
        return f'[{time}]-[{type_.upper()}]: {message}'
    def quit(self):
        self.log_file.close()