__author__ = 'chengsilei'

import sys
import time
from datetime import date

from common import dao, utility
from turtle import dataCaculate, sellSignal, buySignal


def engine_start():
    today = '2015-12-30'
    print date.today()

    #db.writeDBFromStockHistDatasForUpdate(today)
    dao.writeDBFromStockHistDatasForUpdateCurrentDay()
    dataCaculate.calAnalyseDataForUpdate()
    print 'engine started'


def daily_run_once_after_over():
    engine_start()

    sellSignal.updateSellSignalStocks()
    buySignal.updateBuySignalStocks()


def realtime_monitor():
    stocks = dao.getCurrentlyHoldStocks()
    if len(stocks) == 0:
        return

    i = 0
    while True:
        #print time.strftime('%H-%M-%S', time.localtime(time.time()))
        if i >= len(stocks):
            i = 0

        price = utility.getRealPrice(stocks[i][1])
        if price <= stocks[i][8]:
            print 'pain	killer :' + (stocks[i][0]) + ' ' + (stocks[i][1]) + ' at price ' + str(stocks[i][8])

        if price >= stocks[i][6]:
            print 'raise :' + str(stocks[i][0]) + ' ' + str(stocks[i][1]) + ' at price ' + str(stocks[i][6]) + ' for amt ' + str(stocks[i][7])

        i += 1
        time.sleep(8)


def main():
    daily_run_once_after_over()

    #realtime_monitor()

if __name__ == '__main__':
    sys.exit(main())