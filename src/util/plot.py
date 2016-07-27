import matplotlib
matplotlib.use('Agg')

import matplotlib.dates as mdates
import matplotlib.finance as mfinance
import matplotlib.pyplot as mplot
import numpy as np

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
        figure, axes = mplot.subplots(nrows=2, ncols=1)
        figure.subplots_adjust(bottom=0.2)

        #candle stick
        k_ax = axes[0]
        k_ax.set_xticks(range(0, len(self.__datas), self.__xstep))
        k_ax.set_xticklabels([self.__datas[index]['date'] for index in k_ax.get_xticks()])
        mfinance.candlestick_ohlc(k_ax, self.__convert_k_datas(), width=0.6, colorup='r', colordown='g') 
        k_ax.xaxis_date()
        k_ax.autoscale_view()
        mplot.setp(mplot.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        k_ax.grid(True)
        #mplot.title(self.__stock_code)

        #asset curve
        asset_ax = axes[1]
        asset_ax.set_xticks(range(0, len(self.__datas), self.__xstep))
        asset_ax.set_xticklabels([self.__datas[index]['date'] for index in asset_ax.get_xticks()])

        ind = np.arange(len(self.__datas))
        share_ax = asset_ax.twinx()
        asset_ax.bar(ind, self.__get_asset_datas(), width=0.4, color='y', label='asset')
        asset_ax.set_ylabel('total asset')

        share_ax.bar(ind+0.4, self.__get_shares_datas(), width=0.4, color='r', label='shares')
        share_ax.set_ylabel('total share')
        asset_ax.xaxis_date()
        asset_ax.autoscale_view()
        mplot.setp(mplot.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        mplot.savefig(file_name)

    def __convert_k_datas(self):
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

    def __get_asset_datas(self):
        result = []
        for data in self.__datas:
            result.append(data['totalAssets'])
        return result

    def __get_shares_datas(self):
        result = []
        for data in self.__datas:
            result.append(data['totalShares'])
        return result

if __name__ == "__main__":
    datas = [{'closePrice': 4.88, 'highestPrice': 4.79, 'openPrice': 4.85, 'totalAssets': 100000, 'date': '2015-12-01', 'totalShares': 1000, 'lowestPrice': 4.87}, {'closePrice': 5.04, 'highestPrice': 4.83, 'openPrice': 4.87, 'totalAssets': 100000, 'date': '2015-12-02', 'totalShares': 1000, 'lowestPrice': 5.03}, {'closePrice': 5.16, 'highestPrice': 4.94, 'openPrice': 4.98, 'totalAssets': 100000, 'date': '2015-12-03', 'totalShares': 1000, 'lowestPrice': 5.07}, {'closePrice': 5.06, 'highestPrice': 4.95, 'openPrice': 5.03, 'totalAssets': 100000, 'date': '2015-12-04', 'totalShares': 1000, 'lowestPrice': 4.97}, {'closePrice': 4.99, 'highestPrice': 4.92, 'openPrice': 4.96, 'totalAssets': 100000, 'date': '2015-12-07', 'totalShares': 1000, 'lowestPrice': 4.96}, {'closePrice': 4.9, 'highestPrice': 4.84, 'openPrice': 4.87, 'totalAssets': 100000, 'date': '2015-12-08', 'totalShares': 1000, 'lowestPrice': 4.85}, {'closePrice': 4.88, 'highestPrice': 4.8, 'openPrice': 4.84, 'totalAssets': 100000, 'date': '2015-12-09', 'totalShares': 1000, 'lowestPrice': 4.83}, {'closePrice': 4.87, 'highestPrice': 4.81, 'openPrice': 4.84, 'totalAssets': 100000, 'date': '2015-12-10', 'totalShares': 1000, 'lowestPrice': 4.83}, {'closePrice': 4.82, 'highestPrice': 4.72, 'openPrice': 4.81, 'totalAssets': 100000, 'date': '2015-12-11', 'totalShares': 1000, 'lowestPrice': 4.77}, {'closePrice': 4.85, 'highestPrice': 4.71, 'openPrice': 4.74, 'totalAssets': 100000, 'date': '2015-12-14', 'totalShares': 1000, 'lowestPrice': 4.85}, {'closePrice': 4.88, 'highestPrice': 4.8, 'openPrice': 4.84, 'totalAssets': 100000, 'date': '2015-12-15', 'totalShares': 1000, 'lowestPrice': 4.83}, {'closePrice': 4.99, 'highestPrice': 4.89, 'openPrice': 4.9, 'totalAssets': 100000, 'date': '2015-12-16', 'totalShares': 1000, 'lowestPrice': 4.93}, {'closePrice': 4.99, 'highestPrice': 4.91, 'openPrice': 4.93, 'totalAssets': 100000, 'date': '2015-12-17', 'totalShares': 1000, 'lowestPrice': 4.96}, {'closePrice': 5.02, 'highestPrice': 4.93, 'openPrice': 4.95, 'totalAssets': 100000, 'date': '2015-12-18', 'totalShares': 1000, 'lowestPrice': 4.94}, {'closePrice': 5.01, 'highestPrice': 4.88, 'openPrice': 4.92, 'totalAssets': 100000, 'date': '2015-12-21', 'totalShares': 1000, 'lowestPrice': 4.99}, {'closePrice': 5.01, 'highestPrice': 4.95, 'openPrice': 5.0, 'totalAssets': 100000, 'date': '2015-12-22', 'totalShares': 1000, 'lowestPrice': 4.99}, {'closePrice': 5.04, 'highestPrice': 4.96, 'openPrice': 4.99, 'totalAssets': 100000, 'date': '2015-12-23', 'totalShares': 1000, 'lowestPrice': 5.0}, {'closePrice': 5.04, 'highestPrice': 4.96, 'openPrice': 5.03, 'totalAssets': 100000, 'date': '2015-12-24', 'totalShares': 1000, 'lowestPrice': 4.98}, {'closePrice': 5.0, 'highestPrice': 4.94, 'openPrice': 4.99, 'totalAssets': 100000, 'date': '2015-12-25', 'totalShares': 1000, 'lowestPrice': 4.97}, {'closePrice': 4.99, 'highestPrice': 4.86, 'openPrice': 4.97, 'totalAssets': 100000, 'date': '2015-12-28', 'totalShares': 1000, 'lowestPrice': 4.86}, {'closePrice': 4.9, 'highestPrice': 4.84, 'openPrice': 4.86, 'totalAssets': 100000, 'date': '2015-12-29', 'totalShares': 1000, 'lowestPrice': 4.9}, {'closePrice': 4.94, 'highestPrice': 4.87, 'openPrice': 4.91, 'totalAssets': 100000, 'date': '2015-12-30', 'totalShares': 1000, 'lowestPrice': 4.91}, {'closePrice': 4.94, 'highestPrice': 4.89, 'openPrice': 4.91, 'totalAssets': 100000, 'date': '2015-12-31', 'totalShares': 1000, 'lowestPrice': 4.9}, {'closePrice': 4.9, 'highestPrice': 4.9, 'openPrice': 4.9, 'totalAssets': 100000, 'date': '2016-01-01', 'totalShares': 1000, 'lowestPrice': 4.9}]
    plot = CandlePlot('002657', datas)
    plot.plot('002657.png')
