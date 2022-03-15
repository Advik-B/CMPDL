# This is the logger module. (Not in pypi)
assert __name__ != "__main__", "This module should not be run directly. Import it instead."
import datetime
import os
from termcolor import colored
import colorama

class Logger:
    def __init__(self):
        colorama.init()
        date = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        self.log_file_name = "logs/" + date
        if os.path.isfile("logs"):
            try:
                os.remove("logs")
                os.mkdir("logs")
            except [OSError, PermissionError]:
                print("[ERROR] Unable to create logs directory")
        elif os.path.isdir("logs"):
            pass
        else:
            os.mkdir("logs")
        self.log_file = open(self.log_file_name, "a")
        self.setup()

    # Override
    def setup(self):
        pass

    def log2(self, message, type_):
        pass

    def log(self, message, type_):
        # Get the current time with milliseconds
        # time = datetime.datetime.now().strftime('%H:%M:%S:%f')
        time = datetime.datetime.now().strftime("%H:%M:%S")
        # format_ = f'[{time}]-[{type_.upper()}]: {message}'
        types = {"info": "green", "warning": "yellow", "error": "red", "debug": "cyan"}
        format_ = f'[{colored(time, "yellow")}]-\
[{colored(type_.upper(), types[type_])}]: \
{colored(message, "white")}'
        file_format = f"[{time}]-[{type_.upper()}]: {message}\n"
        try:
            print(format_)
        except AttributeError:
            pass
        try:
            self.log_file.write(file_format)
        except UnicodeEncodeError:
            for char in file_format:
                try:
                    self.log_file.write(char)
                except UnicodeEncodeError:
                    pass

        del format_, file_format
        self.log2(message, type_)
        return f"[{time}]-[{type_.upper()}]: {message}"

    def info(self, message):
        self.log(message, "info")
    
    def warning(self, message):
        self.log(message, "warning")
    
    def error(self, message):
        self.log(message, "error")
    
    def debug(self, message):
        self.log(message, "debug")

    def quit(self):
        self.log_file.close()
        colorama.deinit()