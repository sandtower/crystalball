import logging

_logger = logging.getLogger(__name__)

class DealStrategy(object):
    def __init__(self, init_fund=100000, buy_percent=0.2, sell_percent=1):
        self.__init_fund = init_fund
        self.__buy_percent = buy_percent
        self.__sell_percent = sell_percent

    def deal(self, context, stock_code, decisions):
        holding = {'shares':0, 'cost':0.0, 'fund':self.__init_fund, 'fq_factor':0.0}
        if context.get_holding_data(stock_code):
            holding = contex.get_holding_data(stock_code)

        result = []
        for decision in decisions:
            deal_type = decision['deal']
            price = decision['price']
            date = decision['date']
            fq_factor = decision['fq_factor']
            if holding['shares'] > 0:
                self.__adjust_for_fq(holding, fq_factor)

            if deal_type == 1:
                volume = self.__buy_in(stock_code, price, holding)
                if volume:
                    self.__append_result(result, volume, price, decision, holding)
                    continue
            if deal_type == 2:
                volume = self.__sell_out(stock_code, price, holding)
                if volume:
                    self.__append_result(result, -volume, price, decision, holding)
                    continue
            self.__append_result(result, 0, price, decision, holding)
        return result

    def __adjust_for_fq(self, holding, new_factor):
        old_factor = holding['fq_factor']
        _logger.info('old factor=%r' % old_factor)
        if old_factor != 0.0 and new_factor > old_factor:
            _logger.info('adjust for fq, before adjusting(shares=%r, cost=%r, fq_factor=%r).' % (holding['shares'], holding['cost'], old_factor))
            ratio = new_factor / old_factor
            holding['shares'] = int(holding['shares'] * ratio)
            holding['cost'] = holding['cost'] / ratio
            _logger.info('adjust for fq, after adjusting(shares=%r, cost=%r, fq_factor=%r).' % (holding['shares'], holding['cost'], new_factor))
        holding['fq_factor'] = new_factor

    def __buy_in(self, stock_code, price, holding):
        shares = holding['shares']
        cost = holding['cost']
        fund = holding['fund']

        volume = 0
        total_assets = cost * shares + fund
        if fund >= total_assets * self.__buy_percent:
            volume = int((total_assets * self.__buy_percent) / (price * 100)) * 100
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
        total_assets = market_cap + fund
        if market_cap <= (total_assets * self.__sell_percent):
            volume = shares
        else:
            volume = int(total_assets * self.__sell_percent / (price * 100)) * 100
        
        holding['shares'] -= volume
        if volume == shares:
            holding['cost'] = 0
        else:
            holding['cost'] = (market_cap - price * volume) / (shares - volume)
        holding['fund'] += price * volume
        _logger.info("sell out stock(%r), decrease shares = %r." % (stock_code, volume))
        _logger.info("sell out stock(%r), total shares = %r, cost = %r, cash = %r" % (stock_code, holding['shares'], holding['cost'], holding['fund']))
        return volume

    def __append_result(self, result, order_shares, order_price, decision, holding):
        assets = self.__get_total_assets(holding, order_price)
        record = {'orderShares': order_shares, 'orderPrice': order_price, 'totalShares': holding['shares'], 'costPrice': holding['cost'], 'totalAssets': assets, 'openPrice': decision['open'], 'closePrice': decision['close'], 'highestPrice': decision['high'], 'lowestPrice': decision['low'], 'date': decision['date']}
        result.append(record)

    def __get_total_assets(self, holding, current_price):
        return holding['shares'] * current_price + holding['fund']

if __name__ == "__main__":
    strategy = DealStrategy()
    decisions = [{'date': '2016-01-01', 'price': 13.0, 'deal': 1}, {'date': '2016-01-02', 'price': 13.4, 'deal': 1}, {'date': '2016-01-03', 'price': None, 'deal': 3}, {'date': '2016-01-04', 'price': 11.8, 'deal': 2}, {'date': '2016-01-05', 'price': None, 'deal': 3}]
    context = {}
    print strategy.deal(context, '002657', decisions)
