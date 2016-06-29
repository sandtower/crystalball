from collector.hist_data_collector import HistDataCollector
from collector.hist_tick_collector import HistTickCollector
from strategy.ma_strategy import MaStrategy
from strategy.deal_strategy  import DealStrategy
from util.db import DB, Collection
from util.constants import Constants
from util.logger import logger
from util.mq_server import MqServer, MsgQueueException

from collections import OrderedDict
from datetime import datetime
import json
import logging
import pymongo
import time

_logger = logging.getLogger(__name__)

class CrystalBall(object):
    DEFAULT_STRATEGY = 'ma_strategy'
    def __init__(self):
        self.__mq_server = None
        self.__db = DB(Constants.DB_NAME)
        self.__trading_strategy = None
        self.__hist_collector = None
        self.__tick_collector = None

    def start(self):
        self.__mq_server = MqServer()
        self.__mq_server.set_callback(self.__process)
        self.__mq_server.start()

    def __process(self, msg, server):
        content = json.loads(msg)
        if not content:
            _logger.warn("request msg(%r) is illegal." % msg)
            return

        stock_code = content.get('stock', None)
        if not stock_code:
            _logger.warn("stock code(%r) is invalid." % stock_code)
            return

        start = content.get('start', None)
        end = content.get('end', None)
        if not start or not end:
            _logger.warn("start date(%r) or end date(%r) is null." % (start, end))
            return

        strategy = content.get('strategy', self.DEFAULT_STRATEGY)
        buy_percent = content.get('buy_ratio', 0.5)
        sell_percent = content.get('sell_ratio', 1)
        
        self.__hist_collector = HistDataCollector(stock_code, self.__db)
        self.__hist_collector.collect()
        context = {}
        history_data = self.__get_data(stock_code, start, end)
        context['history'] = {stock_code: history_data}
        self.__tick_collector = HistTickCollector(stock_code)
        self.__trading_strategy = MaStrategy(self.__price_generator)
        deal_strategy = DealStrategy()
        sugestions = self.__trading_strategy.decide(context, stock_code)
        deals = deal_strategy.deal(context, stock_code, sugestions)
        _logger.info(deals)
        server.send(json.dumps(deals))

    def __get_data(self, stock_code, start, end):
        collection = Collection(stock_code, self.__db)
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        result = {}
        for record in collection.find().sort('date', pymongo.ASCENDING):
            record_date = datetime.strptime(record['date'], '%Y-%m-%d')
            if record_date >= start_date: 
                result[record['date']] = record
            if record_date > end_date:
                break
        return OrderedDict(sorted(result.items(), key= lambda t: t[0]))

    def __price_generator(self, date):
        return self.__tick_collector.get_middle_price(date)

    def stop(self):
        self.__mq_server.stop()

if __name__ == "__main__":
    predict_ball = CrystalBall()
    predict_ball.start()
    time.sleep(10)
    predict_ball.stop()
