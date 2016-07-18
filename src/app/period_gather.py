from collector.hist_data_collector import HistDataCollector
from collector.stock_basic_collector import StockBasicCollector

from util.constants import Constants
from util.db import DB, Collection
from util.logger import logger

from apscheduler.schedulers.blocking import BlockingScheduler
import time

import logging

_logger = logging.getLogger(__name__)

class StockBasicGather(object):
    def __init__(self, db): 
        self.__db = db
        self.__scheduler = BlockingScheduler()
        self.__scheduler.add_job(self.gather, 'cron', day_of_week='mon-fri', hour=22, minute=34)

    def start(self):
        print 'start,,,,,,,,,,,,,,'
        self.__scheduler.start()

    def gather(self):
        print 'gather..........., 0000000'
        StockBasicCollector(self.__db).collect()
        print 'gather..........., 1111111'
    
        stock_list = self.__get_stock_list()
        for stock in stock_list:
            print 'collect stock hist data', stock
            HistDataCollector(stock, self.__db).collect()
        print 'gather..........., end'
    
    def __get_stock_list(self):
        collection = Collection(StockBasicCollector.BASIC_COLLECTION, self.__db)
        stock_infos = collection.find()
        stock_list = []
        for stock_info in stock_infos:
            print stock_info
            stock_list.append(stock_info['code'])
        return stock_list

    def stop(self):
        if self.__scheduler:
            self.__scheduler.shutdown()

class PeriodGather(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    db = DB(Constants.HIST_DATA_DB_NAME)
    gather = StockBasicGather(db)
    gather.start()
    while True:
        time.sleep(1)
