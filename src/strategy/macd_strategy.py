from context import StockContext as Context
from strategy import BaseStrategy

from collections import OrderedDict
from datetime import datetime, timedelta
import numpy
import talib
import logging

_logger = logging.getLogger(__name__)

class MacdStrategy(BaseStrategy):
    def __init__(self, price_generator):
        self.__price_generator = price_generator

    def decide(self, context, stock_code, start_date):
        data = context.get_history_data(stock_code)
        if not data:
            return []

        result = []

        prices = []
        for item in data.items():
            fq_price = item[1]['fqPrice']
            prices.append(fq_price)
            start = datetime.strptime(start_date, '%Y-%m-%d')
            current = datetime.strptime(item[0], '%Y-%m-%d')
            if current < start:
                continue

            macd = self.__macd(prices)
            current_price = self.__price_generator(item[0])
            fq_factor = item[1]['accumAdjFactor']
            turnover = item[1]['turnoverRate']
            open = item[1]['openPrice']
            close = item[1]['closePrice']
            high = item[1]['highestPrice']
            low = item[1]['lowestPrice']

            _logger.info("date = %r, macd = %r, current price = %r" % (item[0], macd, current_price)) 
            if not current_price:
                _logger.warn('get stock(%r) date(%r) tick price fail.' % (stock_code, item[0]))
                continue

            if macd < 0:
                self.__append_result(result, item[0], self.SELL_OUT, current_price, fq_factor, open, close, high, low, turnover, fq_price)
            elif macd > 0 and turnover > 0.05:
                self.__append_result(result, item[0], self.BUY_IN, current_price, fq_factor, open, close, high, low, turnover, fq_price)
            else:
                self.__append_result(result, item[0], self.DO_NOTHING, current_price, fq_factor, open, close, high, low, turnover, fq_price)
        return result

    def __macd(self, prices, fastperiod=12, slowperiod=26, signalperiod=9):
        macd, signal, hist = talib.MACD(numpy.array(prices), fastperiod=fastperiod, 
                                        slowperiod=slowperiod, signalperiod=signalperiod)
        return macd[-1] - signal[-1]

    def __append_result(self, result, date, deal_type, deal_price, fq_factor, open_price, close_price, high_price, low_price, turnover_rate, fq_price):
        record = {'date': date, 'deal': deal_type,
                  'price': deal_price, 'fq_factor': fq_factor,
                  'open': open_price, 'close': close_price,
                  'high': high_price, 'low': low_price,
                  'turnover': turnover_rate,
                  'fq_price': fq_price}
        result.append(record)

if __name__ == "__main__":
    def get_current_price(date):
        return 13.0

    def generate_history_data(history_data, start_date, end_date):
        import random
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        dirs = [-1, 1]
        current = start
        last_price = 13.0
        while current < end:
            random.shuffle(dirs)
            ratio = random.random() / 10
            print dirs[0], ratio, last_price
            price = last_price + (dirs[0] * ratio * last_price)
            print 'price =', price
            last_price = price
            history_data[current.strftime('%Y-%m-%d')] = {'close': price, 'ma5': 12, 'fqPrice': price, 'turnoverRate': 5.0, 'accumAdjFactor': 1.0}
            current += timedelta(days=1)

    history_data = {}
    generate_history_data(history_data, '2016-01-01', '2016-04-30')

    print history_data
    stock_hist_data = OrderedDict(sorted(history_data.items(), key=lambda t: t[0]))

    context = Context()
    context.set_history_data('002657', stock_hist_data)

    macd = MacdStrategy(get_current_price)
    result = macd.decide(context, '002657', '2016-02-01')
    print result
