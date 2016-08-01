from util.config import Config
from util.db import DB, Collection 
from util.constants import Constants
import tushare as ts

from collections import OrderedDict
import json
import os

import logging

_logger = logging.getLogger(__name__)

class HistTickCollector(object):
    SECTION_NAME = 'persistent'
    ITEM_NAME = 'hist_tick_dir'

    def __init__(self, stock_code, db, config):
        self.__stock_code = stock_code
        self.__db = db
        self.__config = config
        self.__base_dir = None
        self.__collection = Collection(stock_code, db)
        self.__setup()

    def __setup(self):
        root_dir = self.__config.get_config(self.SECTION_NAME, self.ITEM_NAME)
        if not root_dir:
            _logger.warn('hist tick collector get config failed.')
            return

        if not os.path.exists(root_dir):
            os.mkdir(root_dir, 0755)

        base_dir = os.path.join(root_dir, self.__stock_code)
        if not os.path.exists(base_dir):
            os.mkdir(base_dir, 0755)
        self.__base_dir = base_dir
        
    def collect(self, date):
        if self.__is_exists(date):
            return self.__load_local_data(date)
        return self.__fetch_and_save(date)

    def __is_exists(self, date):
        data_file = os.path.join(self.__base_dir, date)
        return os.path.exists(data_file) and os.path.isfile(data_file)

    def __load_local_data(self, date):
        data_file = os.path.join(self.__base_dir, date)
        file = open(data_file, 'r')
        try:
            datas = json.load(file)
            return OrderedDict(sorted(datas.items(), key= lambda t: t[0]))
        except Exception as e:
            _logger.exception(e)
        file.close()

    def __fetch_and_save(self, date):
        try:
            df = ts.get_tick_data(self.__stock_code, date, retry_count=5)
            result = self.__parse_dataframe(df)
            self.__save_to_file(date, result)
            return result
        except Exception as e:
            _logger.exception(e)
        return None

    def __parse_dataframe(self, df):
        result = {}
        for i in range(len(df)):
            record = df.iloc[i]
            key = record['time']
            result[key] = record.to_dict()
        return OrderedDict(sorted(result.items(), key= lambda t: t[0]))

    def __save_to_file(self, date, result):
        data_file = os.path.join(self.__base_dir, date)
        with open(data_file, 'w') as outfile:
            outfile.write(json.dumps(result))

    def get_middle_price(self, date):
        datas = self.collect(date)
        if datas and len(datas) > 1:
            middle_data = self.__get_middle_data(datas)
            return middle_data[1]
        return None

    def __get_middle_data(self, datas):
        middle = len(datas) / 2
        middle_data = datas.items()[middle][1]

        price = middle_data['price']
        volume = middle_data['volume']
        time = middle_data['time']
        return time, price, volume

if __name__ == '__main__':
    db = DB(Constants.HIST_TICK_DB_NAME)
    config = Config()
    collector = HistTickCollector('600036', db, config)
    collector.collect('2016-06-28')
    print collector.get_middle_price('2016-06-28')
