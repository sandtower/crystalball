import json
import easytrader as seller_trader


"""
         request:
             {'user': 'xxx',
              'stock_info': [{'stock': 'xxx', 'shares': 100, 'cost': 10.0,       'last_deal': '2016-07-10'},...],
              'fund': 10000,
              'strategy': 'macd',
             }

         response:
             {'user': 'xxx',
              'result': 'ok',
              'deal_info': [{'stock': 'xxx', 'volume': 100, 'deal': 'sell/buy',  'price': 10.0, 'date': '2016-07-10'},...]
"""

"""
        position: [dictionary]
        [{'cost_price': '摊薄成本价',
          'current_amount': '当前数量',
          'enable_amount': '可卖数量',
          'income_balance': '摊薄浮动盈亏',
          'keep_cost_price': '保本价',
          'last_price': '最新价',
          'market_value': '证券市值',
          'position_str': '定位串',
          'stock_code': '证券代码',
          'stock_name': '证券名称'}]
"""

class Trader(object):
    def __init__(self, user, mq):
    	self.__user = user
    	self.__user_of_seller = None
    	self.__mq = mq

    def start_trade(self):
        strategy = self.__get_trade_strategy()
        if strategy is not None:
        	self.__do_trade(strategy)

    def __encode_strategy_request_msg(self):
    	pass

    def __get_trade_strategy(self):
    	msg = self.__encode_strategy_request_msg()
    	self.__mq.send(json.dumps(msg))
    	rsp = self.__mq.recv()
        strategy = json.loads(rsp)
        return strategy

    def __trade_one_stock(self, deal_info):
    	stock_code = deal_info['stock']
    	price = deal_info['price']
    	volume = deal_info['volume']
    	action = deal_info['deal']

    	if action == 'buy':
    		self.__user_of_seller.buy(stock_code, price, volume)
    	elif action == 'sell':
    		self.__user_of_seller.sell(stock_code, price, volume)
    	else:
    		print('Invalid deal code %s' % action

    def __do_trade(self, strategy):
    	if strategy['result'] != 'ok':
    		return

    	user_of_seller = self.__user.login_stock_seller()
    	self.__user_of_seller = user_of_seller
    	deals = strategy["deal_info"]
    	for deal in deals:
    		self.__trade_one_stock(deal)

if __name__ == "__main__":
	pass


