from __future__ import division
__author__ = 'chengsilei'


import sys
import db

# m25 begin from 25th
def calMList(data):
    sum25 = 0
    sum300 = 0

    for i in range(0, 25):
        sum25 += data[i][4]
    for i in range(0, 300):
        sum300 += data[i][4]

    m25 = [sum25 / 25]
    m300 = [sum300 / 300]

    i = 25
    while i < len(data):
        sum25 = sum25 + data[i][4] - data[i-25][4]
        m25.append(sum25 / 25)

        if i >= 300:
            sum300 = sum300 + data[i][4] - data[i-300][4]
            m300.append(sum300 / 300)

        i += 1

    return (m25, m300)


# TR begin from the 2th, N begin from the 21th
def calN(data):
    TR = []
    for i in range(1, len(data)-1):
        TR.append(max(data[i][3]-data[i][5], data[i][3]-data[i-1][4], data[i-1][4]-data[i][5]))

    n = 0
    for i in range(0, 20):
        n += TR[i]

    N = [n / 20]
    i = 20
    while i < len(TR):
        n = (n * 19 + TR[i]) / 20
        N.append(n)
        i += 1

    return N

def calAnalyseDataForSeveralDays(data):
    (m25, m300) = calMList(data)
    N = calN(data)

    i = 21
    while i < len(data):        # 21, 24, 299
        date = data[i][1]
        n = N[i-21]
        m_25 = None
        m_300 = None
        if i >= 24:
            m_25 = m25[i-24]
        if i >= 299:
            m_300 = m300[i-299]

        db.add_stock_analyse_data(data[i][0], date, m_25, m_300, n)
        i += 1


def calAnalyseDataForOneDay(data, analysData):
    preData = analysData[-1:]

    if preData[0][1] == data[len(data)-1][1]:
        return

    TR = (max(data[len(data)-1][3]-data[len(data)-1][5], data[len(data)-1][3]-data[len(data)-2][4],
              data[len(data)-2][4]-data[len(data)-1][5]))
    n = (preData[0][4] * 19 + TR) / 20
    m25 = (preData[0][2] * 24 + data[len(data)-1][4]) / 25
    m300 = (preData[0][3] * 299 + data[len(data)-1][4]) / 300

    db.add_stock_analyse_data(data[0][0], data[len(data)-1][1], m25, m300, n)


def calAnalyseDataInit():
    stockList = db.getCandidateFromDB()

    for stock in stockList:
        data = db.get_hist_data(stock)
        if len(data) <= 300:
            continue

        calAnalyseDataForSeveralDays(data)


def calAnalyseDataForUpdate():
    stockList = db.getCandidateFromDB()

    for stock in stockList:
        data = db.get_hist_data(stock)
        if len(data) <= 300:
            continue

        analysData = db.get_stock_analyse_data(stock)
        if len(analysData) == 0:
            calAnalyseDataForSeveralDays(data)
        else:
            calAnalyseDataForOneDay(data, analysData)

        print str(stock),

    print 'update analyse data'

def main():
    calAnalyseDataInit()


if __name__ == '__main__':
    sys.exit(main())