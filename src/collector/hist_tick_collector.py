from util.db import DB, Collection 
from util.constants import Constants
import tushare as ts
from collections import OrderedDict
import logging

_logger = logging.getLogger(__name__)

class HistTickCollector(object):
    def __init__(self, stock_code, db):
        self.__stock_code = stock_code
        self.__db = db
        self.__collection = Collection(stock_code, db)

    def collect(self, date):
        df = ts.get_tick_data(self.__stock_code, date)
        result = self.__parse_dataframe(df)
        print result
        self.__collection.insert_and_update('date', date, **result)

    def __parse_dataframe(self, df):
        result = {}
        for i in range(len(df)):
            record = df.iloc[i]
            key = record['time']
            result[key] = record.to_dict()
        return OrderedDict(sorted(result.items(), key= lambda t: t[0]))

    def get_middle_price(self, date):
        df = ts.get_tick_data(self.__stock_code, date)
        if len(df) > 1:
            data = self.__get_middle_data(df)
            _logger.info("get date(%r) middle, time(%r), price(%r)" % (date, data[0], data[1]))
            return data[1]
        return None

    def __get_middle_data(self, df):
        middle = len(df) / 2
        datas = df.head(middle).tail(1).to_dict()
        price = datas['price'].values()[0]
        volume = datas['volume'].values()[0]
        time = datas['time'].values()[0]
        return time, price, volume

if __name__ == '__main__':
    db = DB(Constants.HIST_TICK_DB_NAME)
    collector = HistTickCollector('600036', db)
    collector.collect('2016-06-28')
    print collector.get_middle_price('2016-06-28')
