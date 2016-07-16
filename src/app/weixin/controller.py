# coding=utf-8
from collector.hist_data_collector import HistDataCollector
from collector.rt_tick_collector import RTTickCollector
from strategy.context import StockContext as Context
from strategy.ma_strategy import MaStrategy as Strategy
from util.db import DB
from util.constants import Constants

import logging
_logger = logging.getLogger(__name__)

def check_valid(stock_code):
    if not stock_code.isdigit():
        return False
    for key, _ in Constants.STOCK_CODE_CATEGORIES:
        if stock_code.startswith(key):
            return True
    return False

def process(content_dict={"":""}):
    INVALID_STOCK_CODE_MSG = 'You input invalid stock code, please input such as 600001.'
    _logger.info("process, entered..........")
    stock_code = content_dict['Content']
    if not check_valid(stock_code):
        content_dict['Content'] = INVALID_STOCK_CODE_MSG
        return
    db = DB(Constants.HIST_DATA_DB_NAME)
    hist_collector = HistDataCollector(stock_code, db)
    hist_collector.collect()
    realtime_collector = RTTickCollector()
    current_info = {}
    realtime_collector.collect(stock_code, current_info)
    strategy = Strategy(None, db)
    context = Context()
    context.set_realtime_data(stock_code, current_info)
    deal_type = strategy.decide(context, stock_code)

    result = ''
    if deal_type == 1:
        result = 'you should buy now.'
    elif deal_type == 2:
        result = 'you should sell now.'
    else:
        result = 'you hold, do nothing.'
    content_dict['Content'] = result

if __name__ == '__main__':
    print "hello"

