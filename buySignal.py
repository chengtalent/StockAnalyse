from __future__ import division
from common.StockInfo import StockInfo

__author__ = 'chengsilei'

import tushare as ts
import sys
import os
import time
from datetime import timedelta, date
import db
import utility

# bug signal for the price go thrown the 20 days max

def getCandidateFromLocal():
    stockList = []
    fobj = open('stockDataBuySignal.txt', 'r')
    for line in fobj:
        stockList.append(line.split(':')[0].strip())

    fobj.close()
    return stockList

def getCandidateFromNetwork():
    stockList = ts.get_stock_basics()
    stockList = stockList.index
    return stockList

def caclBuySignalYieldedRate(code):
    data = ts.get_hist_data(code)
    data = data.values
    avarRate = 0

    next = -1
    count = 0
    for i in range(30, len(data) - 50):
        if i < next:
            continue

        max = 0
        firstUp = -1
        for j in range(i-20, 20):
            if j >= len(data):
                break
            if data[j][2] > max:
                max = data[j][2]
            if firstUp == -1 and data[j][2] > data[j][9]:
                firstUp = i - j

        if data[i][2] > max and data[i][2] > data[i][9] and firstUp > 1:
            (rate, maxRateIndex) = caclYieldedRate(data, i)
            next = maxRateIndex
            avarRate += rate
            count += 1

    if count == 0:
        return 0
    return avarRate / count

def getAllStockBuySignalYieldedRate():
    stockList = getCandidateFromNetwork()
    buffer = []

    sum = 0
    count = 0
    for stock in stockList:
        rate = caclBuySignalYieldedRate(stock)
        if rate != 0:
            sum += rate
            count += 1
            buffer.append(stock + ' : ' + str(rate))
            print stock + ' : ' + str(rate)

    print sum / count

    ls = os.linesep
    fobj = open('stockDataBuySignalYieldedRate.txt', 'w')
    fobj.writelines(['%s%s' %(x, ls) for x in buffer])
    fobj.close()


def caclYieldedRate(data, beginIndex):
    beginPrice = data[beginIndex][2]
    max = beginPrice
    maxIndex = beginIndex
    min = beginPrice
    minIndex = beginIndex

    i = beginIndex + 1
    while i < len(data) and i < beginIndex + 30:
        if data[i][2] > max:
            max = data[i][2]
            maxIndex = i
        if data[i][2] < min:
            min = data[i][2]
            minIndex = i
        i += 1

    needToHold = False
    period = i + 10
    while i < len(data):
        if data[i][2] > max:
            max = data[i][2]
            maxIndex = i
            needToHold = True

        if i > period:
            if needToHold == False:
                break
            needToHold = False
            period = i + 10
        i += 1

    if min >= beginPrice:
        rate = (max - beginPrice) / beginPrice
        return (rate, maxIndex)
    if max <= beginPrice:
        rate = (beginPrice - min) / beginPrice * (-1)
        return (rate, minIndex)
    if abs(max - beginPrice) >= abs(beginPrice - min):
        rate = (max - beginPrice) / beginPrice
        return (rate, maxIndex)
    rate = (beginPrice - min) / beginPrice * (-1)
    return (rate, minIndex)


def getAllBuySignalStocksToday():

    stockList = getCandidateFromLocal()
    stockInfoList = []
    buffer = []

    endDate = time.strftime("%Y-%m-%d")
    startDate = (date.today() - timedelta(days=40)).strftime("%Y-%m-%d")

    for stock in stockList:
        data = ts.get_hist_data(stock, start=startDate, end=endDate)
        array = (data.values)[-20:]

        max = 0
        for i in range(0, len(array)-1):
            if array[i][2] > max:
                max = array[i][2]

        if len(array) > 18 and array[len(array)-1][2] > max and array[len(array)-1][2] > array[len(array)-1][9]:
            stockInfo = StockInfo(stock, array[len(array)-1][2], array[len(array)-1][9], array)
            stockInfoList.append(stockInfo)

    stockInfoList.sort(lambda s1, s2: cmp(s1.b, s2.b))
    for stockInfo in stockInfoList:
        buffer.append(stockInfo.speak())

    ls = os.linesep
    #fobj = open('stockDataBuySignal.txt', 'w')
    fobj = open('stockDataBuySignalBreakExactly.txt', 'w')
    fobj.writelines(['%s%s' %(x, ls) for x in buffer])
    fobj.close()

    return stockInfoList


def updateBuySignalStocks():
    stockList = db.getCandidateFromDB()

    todayStr = utility.getLastDay()

    count = 0
    for stock in stockList:
        data = db.get_break_through_status(stock)
        if len(data) != 0:
            continue

        data = db.get_hist_data(stock)
        if data[len(data)-1][1] != todayStr:
            continue

        array = data[-20:]
        max = 0
        for i in range(0, len(array)-1):
            if array[i][4] > max:
                max = array[i][4]

        if len(array) > 18 and array[len(array)-1][4] > max:
            analyseData = db.get_stock_analyse_data(stock)
            analyseData = analyseData[-1:]

            if len(analyseData) == 0 or analyseData[0][2] > analyseData[0][3]:
                db.add_new_break_through(stock, array[len(array)-1][4], todayStr)
                count += 1

    print 'add ' + str(count) + ' new break stocks'


def main():
    updateBuySignalStocks()

if __name__ == '__main__':
    sys.exit(main())