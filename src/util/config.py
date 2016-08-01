import ConfigParser
import os
import sys

import logging

_logger = logging.getLogger(__name__)

class Config(object):
    def __init__(self, path='./config', filename='crystalball.ini'):
        self.__path = path
        self.__filename = filename
        self.__config = None
        self.__load()

    def __load(self):
        file_path = os.path.join(self.__path, self.__filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            _logger.warn('load config file(%r) failed.' % file_path)
            return

        self.__config = ConfigParser.ConfigParser()
        self.__config.read(file_path)

    def get_config(self, section, item):
        if self.__config:
            return self.__config.get(section, item)
        return None

if __name__ == "__main__":
    config = Config()
    print config.get_config('persistent', 'hist_tick_dir')
