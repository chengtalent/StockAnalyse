from __future__ import division
__author__ = 'chengsilei'

import sys
import db
import utility
import tushare as ts

positions = 200000.0

def buyStockHint(code):

    analyseData = db.get_stock_analyse_data(code)
    N = analyseData[len(analyseData)-1][4]
    unit = positions * 0.01 / N

    price = utility.getRealPrice(code)

    amt = unit / price

    print 'stock : ' + str(code) + ' buy price : ' + str(price) + ' amt : ' + str(amt)


def buyStockExecute(code, price, amt):
    analyseData = db.get_stock_analyse_data(code)
    N = analyseData[len(analyseData)-1][4]
    unit = positions * 0.01 / N

    buyNextPrice = price + N / 2
    buyNextAmt = unit / buyNextPrice
    stopPrice = price - N * 2

    db.add_new_exchange_log(code, price, amt, 1, buyNextPrice, buyNextAmt, stopPrice)
    print 'add the buy execute log'


def sellStockExecute(code, price, amt):
    db.add_new_exchange_log(code, price, amt, -1)
    print 'add the sell execute log'


def main():

    #buyStockHint('600196')

    buyStockExecute('600284', 15.5, 500)

    #sellStockExecute('002312', 33.07, 100)


if __name__ == '__main__':
    sys.exit(main())