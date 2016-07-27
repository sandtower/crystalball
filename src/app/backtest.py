from channel.mq_client import MsgQueue
from util.plot import HistoryPlot as Plot
from util.logger import logger

from datetime import datetime
import json
import logging
import time

_logger = logging.getLogger(__name__)

class BackTest(object):
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

        plot = Plot(self.__stock_code, datas)
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = self.__stock_code + "_" + current_time 
        plot.plot(filename)

if __name__ == "__main__":
    test = BackTest('300155') 
    test.start()
    test.test('2015-01-01', '2015-12-31')
    test.stop()
