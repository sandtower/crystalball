from ma_strategy import MaStrategy
from macd_strategy import MacdStrategy

class StrategyFactory(object):
    @staticmethod
    def create_strategy(strategy_name, price_generator):
        if strategy_name == 'ma_strategy':
            return MaStrategy(price_generator)
        if strategy_name == 'macd_strategy':
            return MacdStrategy(price_generator)

if __name__ == '__main__':
    def price_generator(date):
        return 10

    ma_strategy = StrategyFactory.create_strategy('ma_strategy', price_generator)
    macd_strategy = StrategyFactory.create_strategy('macd_strategy', price_generator)
