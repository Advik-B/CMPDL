#!bin/env python3

from termcolor import colored
from time import strftime
from zipfile import ZipFile
import datetime
import time
import os

class LoggerError(Exception): pass

class Logger():
    
    def __init__(self) -> None:
        self.ini = False
        
    def init(self, telemetry:bool):
        if telemetry:
            pth = os.path.join(os.getcwd(), 'logs')
            if os.path.isdir(pth) is False:
                os.mkdir(pth)
            elif os.path.isfile(pth) is True:
                os.remove(pth)
                os.mkdir(pth)
            self.telemetry = telemetry
        else:
            self.telemetry = False

        self.ini = True

    def __get_info(self, type_:str) -> tuple:
        if self.ini is False:
            raise LoggerError('Logger not initialized')
        if type_ == 'info':
            TYPE = "INFO"
        elif type_ == 'warning':
            TYPE = "WARNING"
        elif type_ == 'error':
            TYPE = "ERROR"
        elif type_ == 'critical':
            TYPE = "CRITICAL"
        elif type_ == 'debug':
            TYPE = "DEBUG"
        else: raise LoggerError('Invalid logging type: %s' % type_)
        HOUR = strftime("%I", time.gmtime())
        MINUTE = strftime("%M", time.gmtime())
        SECOND = strftime("%S", time.gmtime())
        TIMEZONE = strftime("%Z", time.gmtime())
        TIME = '%s:%s:%s' % (HOUR, MINUTE, SECOND)
        AM_OR_PM = strftime("%p", time.gmtime())

        letters = ['Q',
                'W',
                'E',
                'R',
                'T',
                'Y',
                'U',
                'I',
                'O',
                'P',
                'A',
                'S',
                'D',
                'F',
                'G',
                'H',
                'J',
                'K',
                'L',
                'Z',
                'X',
                'C',
                'V',
                'B',
                'N',
                'M']
        TZ = ''
        for let in TIMEZONE:
            for let_ in letters:
                if let == let_:
                    TZ += let_
                    break
        TIMEZONE = TZ
        del TZ
        return {

            1: TYPE,
            2: TIME,
            3: AM_OR_PM,
            4: TIMEZONE,

        }

    def __write(self, string:str):
        if self.ini is False:
            raise LoggerError('Logger not initialized')
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date = datetime.datetime.now().day
        file_struct = os.path.join(os.getcwd(), 'logs', '%s-%s-%s.log' % (date, month, year))
        with open(file_struct, 'a') as f:
            f.write(string)
            f.write('\n')

    def __log(self, message:str, type_:str,telemetry:bool):
        if self.ini is False:
            raise LoggerError('Logger not initialized')
        info = self.__get_info(type_)
        if type_ in {'error', 'critical'}:
            CLR = 'red'
        elif type_ == 'info':
            CLR = 'green'
        elif type_ == 'warning':
            CLR = 'yellow'
        elif type_ == 'debug':
            CLR = 'cyan'
        string = f"{colored(f'[ {info[1]} ]', CLR)} ⟪ {colored(info[2], 'green')} - {colored(info[3], 'cyan')} ⟫ ({colored(info[4], 'yellow')}): {message}"
        print(string)
        if telemetry:
            self.__write(
                string.replace(
                '',
                ''
                ).replace(
                '[0m',
                ''
                ).replace(
                '⟫',
                ']'
                ).replace(
                '⟪',
                '['
                ).replace(
                '[32m',
                ''
                ).replace(
                '[36m',
                '').replace(
                '[33m',
                '').replace(
                '[31m',
                ''),
                )
    
    def log(self, type_, message:str):
        if self.ini is False:
            raise LoggerError('Logger not initialized')
        self.__log(message, type_, self.telemetry)

    def archive(self, all:bool):
        if self.ini is False:
            raise LoggerError('Logger not initialized')
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        date = datetime.datetime.now().day
        current_date = '%s-%s-%s.log' % (date, month, year)
        if os.path.isdir(os.path.join(os.getcwd(), 'logs')) is True:
                # List all the files in the logs folder
            for file_ in os.listdir(os.path.join(os.getcwd(), 'logs')):
                if not all:
                    # If the file is a log file
                    if file_.endswith('.log') and file_ != current_date:
                        # Archive the log file
                        with ZipFile(os.path.join(os.getcwd(), 'logs', '%s.zip' % file_.replace('.log', '')), 'w') as zip_:
                            zip_.write(os.path.join(os.getcwd(), 'logs', file_), file_)
                        # Delete the log file
                        os.remove(os.path.join(os.getcwd(), 'logs', file_))
                elif file_.endswith('.log'):
                    # Archive the log file
                    with ZipFile(os.path.join(os.getcwd(), 'logs', '%s.zip' % file_.replace('.log', '')), 'w') as zip_:
                        zip_.write(os.path.join(os.getcwd(), 'logs', file_), file_)
                    # Delete the log file
                    os.remove(os.path.join(os.getcwd(), 'logs', file_))
    
    def quit(self):
        self.archive(False)
