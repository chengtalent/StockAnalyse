from __future__ import division
__author__ = 'chengsilei'

import sys
import time
from datetime import timedelta, date
import tushare as ts


def getLastDay():
    today = date.today()
    todayStr = today.strftime("%Y-%m-%d")

    #todayStr = '2015-10-08'

    if today.weekday() == 5:
        todayStr = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif today.weekday() == 6:
        todayStr = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    return todayStr

def getRealPrice(stock):
    real = ts.get_realtime_quotes(stock)
    real = real.values[0]
    price = float(real[3].encode("ascii"))
    return price


def main():
    print str(getRealPrice('600570'))

if __name__ == '__main__':
    sys.exit(main())