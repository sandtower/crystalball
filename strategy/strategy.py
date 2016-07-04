from abc import ABCMeta

class BaseStrategy:
    __metaclass__ = ABCMeta
    BUY_IN = 1
    SELL_OUT = 2
    DO_NOTHING = 3
    def decide(self, stock_code, start_date):
        raise NotImplemented
