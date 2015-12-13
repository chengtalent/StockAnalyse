from __future__ import division
__author__ = 'chengsilei'

import tushare as ts
import sys
import os
import time
from datetime import timedelta, date
import db
import utility

# bug signal for the price go thrown the 20 days max

class StockInfo:
    sid = 0
    price = 0.0
    ma20 = 0.0
    data = []
    b = 9999
    avarRate = 0

    def __init__(self, sid=None, price=None, ma20=None, data=None, avarRate=None):
        self.sid = sid
        self.price = price
        self.ma20 = ma20
        self.data = data
        self.avarRate = avarRate

        for i in range(1, len(self.data)):
            if self.data[len(self.data)-i][2] >= self.data[len(self.data)-i][9]:
                self.b = i
                break

    def speak(self):
        print(self.sid + ' : ' + str(self.price) + ' : ' + str(self.b))
        return self.sid + ' : ' + str(self.price) + ' : ' + str(self.b)

def getCandidateFromNetwork():
    stockList = ts.get_stock_basics()
    stockList = stockList.index
    return stockList


def getAllSellSignalStocksToday():

    stockList = getCandidateFromNetwork()
    stockInfoList = []
    buffer = []

    endDate = time.strftime("%Y-%m-%d")
    startDate = (date.today() - timedelta(days=40)).strftime("%Y-%m-%d")

    for stock in stockList:
        data = ts.get_hist_data(stock, start=startDate, end=endDate)
        array = (data.values)[-10:]

        min = 10000
        for i in range(0, len(array)-1):
            if array[i][2] < min:
                min = array[i][2]

        if len(array) > 8 and array[len(array)-1][2] < min and array[len(array)-1][2] < array[len(array)-1][8]:
            stockInfo = StockInfo(stock, array[len(array)-1][2], array[len(array)-1][8], array)
            stockInfo.speak()
            stockInfoList.append(stockInfo)

    stockInfoList.sort(lambda s1, s2: cmp(s1.b, s2.b))
    for stockInfo in stockInfoList:
        buffer.append(stockInfo.speak())

    ls = os.linesep
    #fobj = open('stockDataBuySignal.txt', 'w')
    fobj = open('stockDataSellSignalBreakDown.txt', 'w')
    fobj.writelines(['%s%s' %(x, ls) for x in buffer])
    fobj.close()

    return stockInfoList


def updateSellSignalStocks():
    stockList = db.getCandidateFromBreakThoughtStocks()

    todayStr = utility.getLastDay()

    count = 0
    for stock in stockList:

        data = db.get_hist_data(stock)
        if data[len(data)-1][1] != todayStr:
            continue

        array = data[-10:]
        min = 10000
        for i in range(0, len(array)-1):
            if array[i][4] < min:
                min = array[i][4]

        if len(array) > 8 and array[len(array)-1][4] < min:
            db.update_break_through_for_sell(stock, array[len(array)-1][4], todayStr)
            count += 1

    print 'sell ' + str(count) + ' break down stocks'



def main():
    updateSellSignalStocks()

if __name__ == '__main__':
    sys.exit(main())