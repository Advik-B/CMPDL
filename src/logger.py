# This is the logger module. (Not in pypi)

import datetime

class Logger():
    def __init__(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        self.log_file = 'logs/' + date
        
    def log(self, message, type_):
        # Get the current time with miliseconds
        # time = datetime.datetime.now().strftime('%H:%M:%S:%f')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        format_ = f'[{time}]-[{type_.upper()}]: {message}'
        print(format_)
