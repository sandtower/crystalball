from context import StockContext as Context
from strategy import BaseStrategy
from util.db import DB, Collection

from collections import OrderedDict
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)

class EmptyHistoryDataException(Exception):
    def __init__(self, msg):
        self.__msg = msg
        _logger.warn('empty history data exception, for %r' % msg)

class MaStrategy(BaseStrategy):
    def __init__(self, price_generator, db):
        self.__price_generator = price_generator
        self.__db = db

    def decide(self, context, stock_code, start_date=None):
        if start_date:
            return self.__decide_history(context, stock_code, start_date)
        else:
            return self.__decide_realtime(context, stock_code)

    def __decide_history(self, context, stock_code, start_date):
        data = context.get_history_data(stock_code)
        result = []

        last_ma = 0
        for item in data.items():
            print item[0]
            start = datetime.strptime(start_date, '%Y-%m-%d')
            current = datetime.strptime(item[0], '%Y-%m-%d')
            if current < start:
                continue

            if last_ma == 0:
                last_ma = item[1]['ma5']
            current_price = self.__price_generator(item[0])
            turnover = item[1]['turnoverRate']
            _logger.info("date = %r" % item[0]) 
            if self.__should_buy(current_price, last_ma, turnover):
                result.append({'date': item[0], 'deal': self.BUY_IN, 'price': current_price})
            elif self.__should_sell(current_price, last_ma):
                result.append({'date': item[0], 'deal': self.SELL_OUT, 'price': current_price})
            else:
                result.append({'date': item[0], 'deal': self.DO_NOTHING, 'price': None})
            last_ma = item[1]['ma5']
        return result

    def __should_buy(self, buy_price, average, turnover):
        if buy_price < average:
            return False
        variation = (buy_price - average) / average
        _logger.info("should buy? buy_price(%r), ma10_price(%r), variation(%r), turnover(%r)." % (buy_price, average, variation, turnover))
        if variation >= 0.05 and turnover >= 0.05:
            return True
        return False

    def __should_sell(self, sell_price, average):
        if sell_price > average:
            return False

        variation = (average - sell_price) / average
        _logger.info("should sell? sell_price(%r), ma10_price(%r), variation(%r)" % (sell_price, average, variation))
        if variation > 0.05:
            return True
        return False

    def __decide_realtime(self, context, stock_code):
        data = context.get_realtime_data(stock_code)
        result = []

        buy_one = data['buyOne']
        sell_one = data['sellOne']
        turnover = data['turnoverRate']

        collection = Collection(stock_code, self.__db)
        last_data = collection.find_one('date')
        if not last_data:
            raise EmptyHistoryDataException('not found stock(%r) history data' % stock_code)

        ma5 = last_data['ma5']
        ma10 = last_data['ma10']

        if self.__should_buy(buy_one, ma10, turnover):
            return self.BUY_IN
        elif self.__should_sell(sell_one, ma10):
            return self.SELL_OUT
        return self.DO_NOTHING

if __name__ == "__main__":
    def get_current_price(date):
        return 13.0

    history_data = {}
    history_01 = {'close': 13.0, 'ma5': 12, 'turnoverRate': 5.0}
    history_data['2016-01-01'] = history_01
    history_02 = {'close': 13.4, 'ma5': 12.3, 'turnoverRate': 7.0}
    history_data['2016-01-02'] = history_02
    history_03 = {'close': 12.7, 'ma5': 12.6, 'turnoverRate': 8.0}
    history_data['2016-01-03'] = history_03
    history_04 = {'close': 11.8, 'ma5': 12.45, 'turnoverRate': 4.5}
    history_data['2016-01-04'] = history_04
    history_05 = {'close': 13.0, 'ma5': 12.4, 'turnoverRate': 10.0}
    history_data['2016-01-05'] = history_05

    stock_hist_data = OrderedDict(sorted(history_data.items(), key=lambda t: t[0]))

    context = Context()
    context.set_history_data('002657', stock_hist_data)

    ma = MaStrategy(get_current_price, None)
    result = ma.decide(context, '002657', '2016-01-01')
    print result
    
