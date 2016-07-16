class StockContext(object):
    def __init__(self):
        self.__history_data = {}
        self.__realtime_data = {}
        self.__holding_data = {}

    def set_history_data(self, stock_code, data):
        self.__history_data[stock_code] = data

    def get_history_data(self, stock_code):
        if self.__history_data.get(stock_code):
            return self.__history_data[stock_code]
        return None

    def set_realtime_data(self, stock_code, data):
        self.__realtime_data[stock_code] = data

    def get_realtime_data(self, stock_code):
        if self.__realtime_data.get(stock_code):
            return self.__realtime_data[stock_code]
        return None

    def set_holding_data(self, stock_code, data):
        self.__holding_data[stock_code] = data

    def get_holding_data(self, stock_code):
        if self.__holding_data.get(stock_code):
            return self.__holding_data[stock_code]
        return None

