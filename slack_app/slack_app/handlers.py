import os
from logging.handlers import RotatingFileHandler


def create_logging_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


class MakeFileHandler(RotatingFileHandler):

    def __init__(self, *args, **kwargs):
        RotatingFileHandler.__init__(self, *args, **kwargs)

    def emit(self, record):
        print(self.baseFilename)
        create_logging_directory(self.baseFilename)
        super().emit(record)
