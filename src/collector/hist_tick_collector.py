from util.config import Config
from util.file_db import FileDB
from util.constants import Constants
import tushare as ts

from collections import OrderedDict
import os
import msgpack
import numpy as np

import logging

_logger = logging.getLogger(__name__)

class HistTickCollector(object):
    SECTION_NAME = 'persistent'
    ITEM_NAME = 'hist_tick_dir'

    def __init__(self, stock_code, db):
        self.__stock_code = stock_code
        self.__db = db

    def collect(self, date):
        if self.__is_exists(date):
            return self.__load_data_from_db(date)
        return self.__fetch_and_save(date)

    def __is_exists(self, date):
        key = '_'.join([self.__stock_code, date]) 
        return self.__db.contain(str(key))

    def __load_data_from_db(self, date):
        try:
            key = '_'.join([self.__stock_code, date]) 
            raw_datas = self.__db.get(str(key))
            datas = msgpack.unpackb(raw_datas)
            return OrderedDict(sorted(datas.items(), key= lambda t: t[0]))
        except Exception as e:
            _logger.exception(e)
        return None

    def __fetch_and_save(self, date):
        try:
            df = ts.get_tick_data(self.__stock_code, date, retry_count=5)
            result = self.__parse_dataframe(df)
            self.__save_to_db(date, result)
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

    def __save_to_db(self, date, result):
        key = '_'.join([self.__stock_code, date])
        self.__db.set(str(key), msgpack.packb(result))

    def get_middle_price(self, date):
        datas = self.collect(date)
        if datas and len(datas) > 1:
            middle_data = self.__get_middle_data(datas)
            if not np.isnan(middle_data[1]):
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
    db = FileDB('/data/test')
    collector = HistTickCollector('600036', db)
    collector.collect('2016-06-28')
    print collector.get_middle_price('2016-06-28')
