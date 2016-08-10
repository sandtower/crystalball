from context import StockContext as Context
from strategy import BaseStrategy

from collections import OrderedDict
from datetime import datetime
import heapq
import logging

_logger = logging.getLogger(__name__)

class PendulumStrategy(BaseStrategy):
    UNDERESTIMATE_BEGIN = -90
    UNDERESTIMATE_END = -30
    OVERESTIMATE_BEGIN = -120
    OVERESTIMATE_END = -60
    UNDER_ESTIMATE_PERCENT = 0.1
    OVER_ESTIMATE_PERCENT = 1.0

    def __init__(self, price_generator):
        self.__price_generator = price_generator

    def decide(self, context, stock_code, start_date):
        data = context.get_history_data(stock_code)
        if not data:
            return []

        prices = []
        result = []
        for item in data.items():
            fq_price = item[1]['fqPrice']
            prices.append(fq_price)

            start = datetime.strptime(start_date, '%Y-%m-%d')
            current = datetime.strptime(item[0], '%Y-%m-%d')
            if current < start:
                continue

            current_price = self.__price_generator(item[0])
            fq_factor = item[1]['accumAdjFactor']
            turnover = item[1]['turnoverRate']
            open = item[1]['openPrice']
            close = item[1]['closePrice']
            high = item[1]['highestPrice']
            low = item[1]['lowestPrice']
            ma5 = item[1]['ma5']
            ma20 = item[1]['ma20']

            if not current_price:
                _logger.warn('get stock(%r) date(%r) tick price fail.' % (stock_code, item[0]))
                continue

            if self.__should_sell(current_price, ma5, ma20, hist_prices[self.OVERESTIMATE_BEGIN:self.OVERESITMATE_END]):
                self.__append_result(result, item[0], self.SELL_OUT, current_price, fq_factor, open, close, high, low, turnover, fq_price)
            elif self.__should_buy(current_price, ma5, ma20, hist_prices[self.UNDERESTIMATE_BEGIN:self.UNDERESTIMATE_END]):
                self.__append_result(result, item[0], self.BUY_IN, current_price, fq_factor, open, close, high, low, turnover, fq_price)
            else:
                self.__append_result(result, item[0], self.DO_NOTHING, current_price, fq_factor, open, close, high, low, turnover, fq_price)
        return result
            
    def __should_buy(self, current_price, short_price, long_price, hist_prices):
        if short_price > long_price and current_price <= self.__calc_underestimate_price(hist_prices):
            return True 
        return False

    def __calc_underestimate_price(self, hist_prices):
        smallest = heapq.nsmallest(1, hist_prices) 
        return smallest - smallest * UNDER_ESTIMATE_PERCENT
        
    def __should_sell(self, short_price, long_price, hist_prices):
        if short_price < long_price and current_price >= self.__calc_overestimate_price(hist_prices):
            return True
        return False
        
    def __calc_overestimate_price(self, hist_prices):
        largest = heapq.nlargest(1, hist_prices) 
        return largest + largest * OVER_ESTIMATE_PERCENT
        
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

    history_data = {}
    generate_history_data(history_data, '2016-01-01', '2016-04-30')

    print history_data
    stock_hist_data = OrderedDict(sorted(history_data.items(), key=lambda t: t[0]))

    context = Context()
    context.set_history_data('002657', stock_hist_data)

    strategy = PendulumStrategy(get_current_price)
    result = strategy.decide(context, '002657', '2016-02-01')
    print result
