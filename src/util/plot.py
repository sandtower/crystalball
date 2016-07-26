import matplotlib
matplotlib.use('Agg')

import matplotlib.dates as mdates
import matplotlib.finance as mfinance
import matplotlib.pyplot as mplot

from datetime import datetime

class CandlePlot(object):
    ALLDAYS = mdates.DayLocator()

    def __init__(self, stock_code, datas):
        self.__stock_code = stock_code
        self.__datas = datas

        if len(datas) < 100:
            self.__xstep = 5
        else:
            self.__xstep = 22

    def plot(self, file_name):
        figure, ax = mplot.subplots()
        figure.subplots_adjust(bottom=0.2)

        ax.set_xticks(range(0, len(self.__datas), self.__xstep))
        ax.set_xticklabels([self.__datas[index]['date'] for index in ax.get_xticks()])

        mfinance.candlestick_ohlc(ax, self.__convert_datas(), width=0.6, colorup='r', colordown='g') 

        ax.xaxis_date()
        ax.autoscale_view()
        mplot.setp(mplot.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        ax.grid(True)
        mplot.title(self.__stock_code)

        mplot.savefig(file_name)

    def __convert_datas(self):
        result = []
        index = 0
        for data in self.__datas:
            open = data['openPrice']
            close = data['closePrice']
            high = data['highestPrice']
            low = data['lowestPrice']

            result.append((index, open, close, high, low))
            index += 1
        return result

if __name__ == "__main__":
    datas = [{'date': '2015-12-01', 'closePrice': 4.88, 'lowestPrice': 4.87, 'openPrice': 4.85, 'highestPrice': 4.79}, {'date': '2015-12-02', 'closePrice': 5.04, 'lowestPrice': 5.03, 'openPrice': 4.87, 'highestPrice': 4.83}, {'date': '2015-12-03', 'closePrice': 5.16, 'lowestPrice': 5.07, 'openPrice': 4.98, 'highestPrice': 4.94}, {'date': '2015-12-04', 'closePrice': 5.06, 'lowestPrice': 4.97, 'openPrice': 5.03, 'highestPrice': 4.95}, {'date': '2015-12-07', 'closePrice': 4.99, 'lowestPrice': 4.96, 'openPrice': 4.96, 'highestPrice': 4.92}, {'date': '2015-12-08', 'closePrice': 4.9, 'lowestPrice': 4.85, 'openPrice': 4.87, 'highestPrice': 4.84}, {'date': '2015-12-09', 'closePrice': 4.88, 'lowestPrice': 4.83, 'openPrice': 4.84, 'highestPrice': 4.8}, {'date': '2015-12-10', 'closePrice': 4.87, 'lowestPrice': 4.83, 'openPrice': 4.84, 'highestPrice': 4.81}, {'date': '2015-12-11', 'closePrice': 4.82, 'lowestPrice': 4.77, 'openPrice': 4.81, 'highestPrice': 4.72}, {'date': '2015-12-14', 'closePrice': 4.85, 'lowestPrice': 4.85, 'openPrice': 4.74, 'highestPrice': 4.71}, {'date': '2015-12-15', 'closePrice': 4.88, 'lowestPrice': 4.83, 'openPrice': 4.84, 'highestPrice': 4.8}, {'date': '2015-12-16', 'closePrice': 4.99, 'lowestPrice': 4.93, 'openPrice': 4.9, 'highestPrice': 4.89}, {'date': '2015-12-17', 'closePrice': 4.99, 'lowestPrice': 4.96, 'openPrice': 4.93, 'highestPrice': 4.91}, {'date': '2015-12-18', 'closePrice': 5.02, 'lowestPrice': 4.94, 'openPrice': 4.95, 'highestPrice': 4.93}, {'date': '2015-12-21', 'closePrice': 5.01, 'lowestPrice': 4.99, 'openPrice': 4.92, 'highestPrice': 4.88}, {'date': '2015-12-22', 'closePrice': 5.01, 'lowestPrice': 4.99, 'openPrice': 5.0, 'highestPrice': 4.95}, {'date': '2015-12-23', 'closePrice': 5.04, 'lowestPrice': 5.0, 'openPrice': 4.99, 'highestPrice': 4.96}, {'date': '2015-12-24', 'closePrice': 5.04, 'lowestPrice': 4.98, 'openPrice': 5.03, 'highestPrice': 4.96}, {'date': '2015-12-25', 'closePrice': 5.0, 'lowestPrice': 4.97, 'openPrice': 4.99, 'highestPrice': 4.94}, {'date': '2015-12-28', 'closePrice': 4.99, 'lowestPrice': 4.86, 'openPrice': 4.97, 'highestPrice': 4.86}, {'date': '2015-12-29', 'closePrice': 4.9, 'lowestPrice': 4.9, 'openPrice': 4.86, 'highestPrice': 4.84}, {'date': '2015-12-30', 'closePrice': 4.94, 'lowestPrice': 4.91, 'openPrice': 4.91, 'highestPrice': 4.87}, {'date': '2015-12-31', 'closePrice': 4.94, 'lowestPrice': 4.9, 'openPrice': 4.91, 'highestPrice': 4.89}, {'date': '2016-01-01', 'closePrice': 4.9, 'lowestPrice': 4.9, 'openPrice': 4.9, 'highestPrice': 4.9}]
    plot = CandlePlot('002657', datas)
    plot.plot('002657.png')
