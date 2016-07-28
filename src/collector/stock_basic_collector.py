from util.db import DB, Collection
from util.constants import Constants

import tushare as ts
import logging

_logger = logging.getLogger(__name__)

class StockBasicCollector(object):
    def __init__(self, db):
        self.__db = db
        self.__collection = Collection(Constants.BASIC_COLLECTION, self.__db)

    def collect(self):
        _logger.info('collect stock basic info, begin.....')
        result = ts.get_stock_basics()
        result['code'] = result.index
        for i in range(len(result)):
            record = result.iloc[i].to_dict()
            self.__collection.insert_and_update('code', record['code'], **record)
        _logger.info('collect stock basic info, end.....')

if __name__ == '__main__':
    db = DB(Constants.HIST_DATA_DB_NAME)
    collector = StockBasicCollector(db)
    collector.collect()
