from strategy import BaseStrategy
from collections import OrderedDict

import logging

_logger = logging.getLogger(__name__)

class MaStrategy(BaseStrategy):
    def __init__(self):
        pass

    def decide(self, context, stock_code):
        data = context['history'][stock_code]
        result = []

        last_ma = 0
        for item in data.items():
            if last_ma == 0:
                last_ma = item[1]['ma10']
            current_price = item[1]['close']
            _logger.info("date = %r" % item[0]) 
            if self.__should_buy(current_price, last_ma):
                result.append({'date': item[0], 'deal': self.BUY_IN, 'price': current_price})
            elif self.__should_sell(current_price, last_ma):
                result.append({'date': item[0], 'deal': self.SELL_OUT, 'price': current_price})
            else:
                result.append({'date': item[0], 'deal': self.DO_NOTHING, 'price': None})
            last_ma = item[1]['ma10']
        return result

    def __should_buy(self, buy_price, average):
        if buy_price < average:
            return False
        variation = (buy_price - average) / average
        _logger.info("should buy? buy_price(%r), ma10_price(%r), variation(%r)" % (buy_price, average, variation))
        if variation >= 0.05:
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

if __name__ == "__main__":
    history_data = {}
    history_01 = {'close': 13.0, 'ma10': 12}
    history_data['2016-01-01'] = history_01
    history_02 = {'close': 13.4, 'ma10': 12.3}
    history_data['2016-01-02'] = history_02
    history_03 = {'close': 12.7, 'ma10': 12.6}
    history_data['2016-01-03'] = history_03
    history_04 = {'close': 11.8, 'ma10': 12.45}
    history_data['2016-01-04'] = history_04
    history_05 = {'close': 13.0, 'ma10': 12.4}
    history_data['2016-01-05'] = history_05

    stock_hist_data = {}
    stock_hist_data['002657'] = OrderedDict(sorted(history_data.items(), key=lambda t: t[0]))

    context = {}
    context['history'] = stock_hist_data

    ma = MaStrategy()
    result = ma.decide(context, '002657')
    print result
    
