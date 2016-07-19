from util.db import DB, Collection
from util.constants import Constants
from util.util import Util

import numpy as np
import tushare as ts
import logging

_logger = logging.getLogger(__name__)

class HistDataCollector(object):
    FIELDS = 'tradeDate,ticker,secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,closePrice,turnoverVol,turnoverRate,accumAdjFactor,isOpen'
    def __init__(self, stock_code, db):
        self.__stock_code = stock_code
        self.__db = db
        self.__collection = Collection(stock_code, self.__db)
        self.__hist_close_price = []

    def collect(self):
        begin_date = self.__get_begin_date()

        end_date = Util.get_today()
        _logger.info('collect stock(%s) history data, begin date: %r, end date: %r.' % (self.__stock_code, begin_date, end_date))

        market = ts.Market()
        if begin_date == end_date:
            return
        elif not begin_date or len(begin_date) == 0:
            result = market.MktEqud(ticker=self.__stock_code, field=self.FIELDS)
        else:
            result = market.MktEqud(ticker=self.__stock_code, beginDate=begin_date, endDate=end_date, field=self.FIELDS)

        if result is None:
            _logger.warn('could get stock(%r) history data from tushare.' % self.__stock_code)
            return

        for i in range(len(result)):
            record = result.iloc[i].to_dict()
            if record['isOpen'] == 1:
                fq_factor = record['accumAdjFactor']
                record['fqPrice'] = record['closePrice'] * fq_factor
                self.__hist_close_price.append(record['fqPrice'])

                record['ma5'] = self.__get_ma5_price()
                record['ma10'] = self.__get_ma10_price()
                record['ma20'] = self.__get_ma20_price()

                self.__collection.insert_and_update('date', record['tradeDate'], **record)

    def __get_begin_date(self):
        record = self.__collection.find_one('date')
        if record:
            begin_date = ''.join(c for c in record['date'] if c != '-')
            return begin_date
        return None

    def __get_ma5_price(self):
        if len(self.__hist_close_price) > 5:
            return np.mean(self.__hist_close_price[-5:])
        else:
            return np.mean(self.__hist_close_price)
         
    def __get_ma10_price(self):
        if len(self.__hist_close_price) > 10:
            return np.mean(self.__hist_close_price[-10:])
        else:
            return np.mean(self.__hist_close_price)

    def __get_ma20_price(self):
        if len(self.__hist_close_price) > 20:
            return np.mean(self.__hist_close_price[-20:])
        else:
            return np.mean(self.__hist_close_price)

    def __get_history_close_price(self):
        self.__collection.find

if __name__ == '__main__':
    db = DB(Constants.HIST_DATA_DB_NAME)
    collector = HistDataCollector('600036', db)
    collector.collect()
