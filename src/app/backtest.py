from channel.mq_client import MsgQueue
from util.constants import Constants
from util.db import DB, Collection
from util.dump_stack import dumpstacks 
from util.logger import setup_logger
from util.plot import HistoryPlot as Plot

from datetime import datetime
import json
import logging
import time

setup_logger('backtest.log')
_logger = logging.getLogger(__name__)

class SingleBackTest(object):
    def __init__(self, stock_code):
        self.__stock_code = stock_code
        self.__mq = MsgQueue()

    def start(self):
        self.__mq.start()

    def stop(self):
        self.__mq.stop()

    def test(self, start, end):
        stock_info = {'stock': self.__stock_code, 'start': start, 'end': end}
        self.__mq.send(json.dumps(stock_info))
        time.sleep(1)
        msg = self.__mq.recv()
        datas = json.loads(msg)
        _logger.info(datas)

        if datas and len(datas):
            plot = Plot(self.__stock_code, datas)
            current_time = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = self.__stock_code + "_" + current_time 
            plot.plot(filename)

class BatchBackTest(object):
    def __init__(self, db):
        self.__db = db
        self.__mq = MsgQueue()

    def start(self):
        self.__mq.start()

    def stop(self):
        self.__mq.stop()

    def test(self, start, end):
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = 'batch_' + current_time + '.txt'
        file = open(filename, 'w')
        try:
            stock_list = self.__get_stock_list()
            _logger.info(stock_list)
            for stock in stock_list:
                roi, fix = self.__iterate_test(stock, start, end)
                if roi:
                    result = '%s, %f, %f' % (stock, roi, fix)
                    file.write(result)
                    file.write('\n')
                    file.flush()
        except Exception as e:
            _logger.exception(e)

        file.close()

    def __iterate_test(self, stock_code, start, end):
        stock_info = {'stock': stock_code, 'start': start, 'end': end}
        self.__mq.send(json.dumps(stock_info))
        _logger.info(stock_info)
        time.sleep(1)
        msg = self.__mq.recv()
        datas = json.loads(msg)
        _logger.info(datas)
        if len(datas) > 2:
            initial_asset = datas[0]['totalAssets']
            final_asset = datas[-1]['totalAssets']
            roi = float('%0.3f' % (float(final_asset - initial_asset) / initial_asset))

            initial_price = datas[0]['fqPrice']
            final_price = datas[-1]['fqPrice']
            _logger.info('%r, %r' % (initial_price, final_price))
            fix = float('%0.3f' % ((final_price - initial_price) / initial_price))
            return roi, fix
            
        return None, None

    def __get_stock_list(self):
        collection = Collection(Constants.BASIC_COLLECTION, self.__db)
        stock_infos = collection.find()
        stock_list = []
        for stock_info in stock_infos:
            stock_list.append(stock_info['code'])
        return stock_list

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGUSR1, dumpstacks)

    #single_test = SingleBackTest('600701') 
    #single_test.start()
    #single_test.test('2015-01-01', '2015-12-31')
    #single_test.stop()

    db = DB(Constants.HIST_DATA_DB_NAME)
    batch_test = BatchBackTest(db)
    batch_test.start()
    batch_test.test('2015-01-01', '2015-12-31')
    batch_test.stop()
