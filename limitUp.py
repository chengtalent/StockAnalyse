from __future__ import division
__author__ = 'chengsilei'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import sys
import os

#涨停后第二天继续上涨的概率


class StockInfo:
    sid = 0
    limitUp = 0
    nextLimit = 0
    percent = 0.0

    def __init__(self, sid=None, limit=None, next_limit=None, percent=None):
        self.sid = sid
        self.limitUp = limit
        self.nextLimit = next_limit
        self.percent = percent

    def speak(self):
        print(self.sid + ' : ' + str(self.percent))
        return self.sid + ' : ' + str(self.percent)


def main():
    stockList = ts.get_stock_basics()
    stockList = stockList.index

    stockInfoList = []
    buffer = []

    for stock in stockList:
        data = ts.get_hist_data(stock)
        array = data.values

        limitUp = 0
        nextUp = 0
        for i in range(0, len(array)-1):
            if array[i][6] > 9:
                limitUp += 1
                if array[i+1][6] > 0:
                    nextUp += 1

        if limitUp > 0:
            stockInfo = StockInfo(stock, limitUp, nextUp, nextUp/limitUp)
            stockInfoList.append(stockInfo)
            buffer.append(stockInfo.speak())

    ls = os.linesep
    fobj = open('stockData.txt', 'w')
    fobj.writelines(['%s%s' %(x, ls) for x in buffer])
    fobj.close()

    stockInfoList.sort(lambda s1, s2: cmp(s1.percent, s2.percent) * (-1))
    fobj2 = open('stockDataSorted.txt', 'w')
    bufferSorted = []
    for stockInfo in stockInfoList:
        bufferSorted.append(stockInfo.speak())
    fobj2.writelines(['%s%s' %(x, ls) for x in bufferSorted])
    fobj2.close()

if __name__ == '__main__':
    sys.exit(main())