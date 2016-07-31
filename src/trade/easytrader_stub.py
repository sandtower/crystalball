class User(object):
	def __init__(self, seller):
		self.__seller = seller
		self.__cfg = None
		print('Init %s seller stub' % seller)

	def login():
		print('Login Stub easytrader')
		

	def prepare(self, cfg):
		self.__cfg = cfg

	def sell(self, stock_code, price, volume):
		return {"entrust_no" : "00000000", "stock_code" : stock_code, "entrust_price" : price}

	def buy(self, stock_code, price, volume):
		"""
		[{'entrust_no': '委托编号',
	      'init_date': '发生日期',
	      'batch_no': '委托批号',
	      'report_no': '申报号',
	      'seat_no': '席位编号',
	      'entrust_time': '委托时间',
	      'entrust_price': '委托价格',
	      'entrust_amount': '委托数量',
	      'stock_code': '证券代码',
	      'entrust_bs': '买卖方向',
	      'entrust_type': '委托类别',
	      'entrust_status': '委托状态',
	      'fund_account': '资金帐号',
	      'error_no': '错误号',
	      'error_info': '错误原因'}]
	    """
		return {"entrust_no" : "00000000", "stock_code" : stock_code, "entrust_price" : price}


def use(broker, debug=True, **kwargs):
	return User(broker)