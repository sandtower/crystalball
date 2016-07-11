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
        data = context['history'][stock_code]
        result = []

        prices = []
        for item in data.items():
            close = item[1]['close']
            prices.append(close)
            start = datetime.strptime(start_date, '%Y-%m-%d')
            current = datetime.strptime(item[0], '%Y-%m-%d')
            if current < start:
                continue

            macd = self.__macd(prices)
            current_price = self.__price_generator(item[0])
            turnover = item[1]['turnover']
            factor = close / current_price
            _logger.info("date = %r, macd = %r, current price = %r" % (item[0], macd, current_price)) 
            print 'current_price =', current_price

            if macd < 0:
                result.append({'date': item[0], 'deal': self.SELL_OUT, 'price': current_price, 'factor': factor})
            elif macd > 0 and turnover > 5.0:
                result.append({'date': item[0], 'deal': self.BUY_IN, 'price': current_price, 'factor': factor})
            else:
                result.append({'date': item[0], 'deal': self.DO_NOTHING, 'price': None, 'factor': None})
        return result

    def __macd(self, prices, fastperiod=12, slowperiod=26, signalperiod=9):
        macd, signal, hist = talib.MACD(numpy.array(prices), fastperiod=fastperiod, 
                                        slowperiod=slowperiod, signalperiod=signalperiod)
        return macd[-1] - signal[-1]

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
            history_data[current.strftime('%Y-%m-%d')] = {'close': price, 'ma5': 12, 'turnover': 5.0}
            current += timedelta(days=1)

    history_data = {}
    generate_history_data(history_data, '2016-01-01', '2016-04-30')

    print history_data
    stock_hist_data = {}
    stock_hist_data['002657'] = OrderedDict(sorted(history_data.items(), key=lambda t: t[0]))

    context = {}
    context['history'] = stock_hist_data

    macd = MacdStrategy(get_current_price)
    result = macd.decide(context, '002657', '2016-02-01')
    print result
