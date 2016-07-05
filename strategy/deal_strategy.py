import logging

_logger = logging.getLogger(__name__)

class DealStrategy(object):
    def __init__(self, init_fund=100000, buy_percent=0.2, sell_percent=1):
        self.__init_fund = init_fund
        self.__buy_percent = buy_percent
        self.__sell_percent = sell_percent

    def deal(self, context, stock_code, decisions):
        holding = {'shares':0, 'cost':0, 'fund':self.__init_fund}
        if context.get('holdings'):
            holding = contex['holdings'].get(stock_code, holding)

        result = []
        for decision in decisions:
            deal_type = decision['deal']
            price = decision['price']
            date = decision['date']
            if deal_type == 1:
                volume = self.__buy_in(stock_code, price, holding)
                if volume:
                    result.append({'volume': volume, 'price': price, 'date': date})
            elif deal_type == 2:
                volume = self.__sell_out(stock_code, price, holding)
                if volume:
                    result.append({'volume': -volume, 'price': price, 'date': date})
        return result

    def __buy_in(self, stock_code, price, holding):
        shares = holding['shares']
        cost = holding['cost']
        fund = holding['fund']

        volume = 0
        if fund >= self.__init_fund * self.__buy_percent:
            volume = int((self.__init_fund * self.__buy_percent) / (price * 100)) * 100
        else:
            volume = int(fund / (price * 100)) * 100
        if volume == 0:
            return 0
        
        holding['shares'] += volume
        holding['cost'] = (cost * shares + price * volume) / (shares + volume)
        holding['fund'] -= price * volume
        _logger.info("buy in stock(%r), increase shares = %r." % (stock_code, volume))
        _logger.info("buy in stock(%r), total shares = %r, cost = %r, cash = %r" % (stock_code, holding['shares'], holding['cost'], holding['fund']))
        return volume

    def __sell_out(self, stock_code, price, holding):
        shares = holding['shares']
        cost = holding['cost']
        fund = holding['fund']

        if shares == 0:
            return 0

        volume = 0
        market_cap = cost * shares
        if market_cap <= ((market_cap + fund) * self.__sell_percent):
            volume = shares
        else:
            volume = int((market_cap + fund) * self.__sell_percent / (price * 100)) * 100
        
        holding['shares'] -= volume
        if volume == shares:
            holding['cost'] = 0
        else:
            holding['cost'] = (market_cap - price * volume) / (shares - volume)
        holding['fund'] += price * volume
        _logger.info("sell out stock(%r), decrease shares = %r." % (stock_code, volume))
        _logger.info("sell out stock(%r), total shares = %r, cost = %r, cash = %r" % (stock_code, holding['shares'], holding['cost'], holding['fund']))
        return volume

if __name__ == "__main__":
    strategy = DealStrategy()
    decisions = [{'date': '2016-01-01', 'price': 13.0, 'deal': 1}, {'date': '2016-01-02', 'price': 13.4, 'deal': 1}, {'date': '2016-01-03', 'price': None, 'deal': 3}, {'date': '2016-01-04', 'price': 11.8, 'deal': 2}, {'date': '2016-01-05', 'price': None, 'deal': 3}]
    context = {}
    print strategy.deal(context, '002657', decisions)
