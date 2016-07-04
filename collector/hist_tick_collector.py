import tushare as ts
import logging

_logger = logging.getLogger(__name__)

class HistTickCollector(object):
    def __init__(self, stock_code):
        self.__stock_code = stock_code

    def collect(self, date):
        df = ts.get_tick_data(self.__stock_code, date)
        return df.to_dict()

    def get_middle_price(self, date):
        df = ts.get_tick_data(self.__stock_code, date)
        if len(df) > 1:
            data = self.__get_middle_data(df)
            _logger.info("get date(%r) middle, time(%r), price(%r)" % (date, data[0], data[1]))
            return data[1]
        return None

    def __get_middle_data(self, df):
        middle = len(df) / 2
        datas = df.head(middle).tail(1).to_dict()
        price = datas['price'].values()[0]
        volume = datas['volume'].values()[0]
        time = datas['time'].values()[0]
        return time, price, volume

if __name__ == '__main__':
    collector = HistTickCollector('600036')
    print collector.collect('2016-06-28')
    print collector.get_middle_price('2016-06-28')
