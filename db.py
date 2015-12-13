__author__ = 'chengsilei'

import sys
import time
import sqlite3
import tushare as ts
import utility
from sqlalchemy import create_engine


def writeDBFromFile():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    fobj = open('stockDataBuySignal.txt', 'r')
    for line in fobj:
        conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
          VALUES (1, 'Paul', 32, 'California', 20000.00 )")

    fobj.close()
    conn.commit()
    print "Records created successfully"
    conn.close()


def writeDBFromStockBasicsList():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    stockList = ts.get_stock_basics()
    index = stockList.index
    datas = stockList.values

    for i in range(0, len(index)):
        code = index[i]
        data = datas[i]
        name = (data[0]).decode('utf-8')
        industry = (data[1]).decode('utf-8')
        area = (data[2]).decode('utf-8')

        t = (code, name, industry, area, data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
             data[11], data[12], data[13], data[14])
        c.execute('INSERT INTO stock_basics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', t)

    conn.commit()
    print "Records created successfully"
    conn.close()


def writeDBFromStockHistDatas():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    stockList = ts.get_stock_basics()
    stockList = stockList.index

    for stock in stockList:
        datas = ts.get_hist_data(stock)
        index = datas.index
        datas = datas.values

        for i in range(0, len(datas)):
            data = datas[i]
            t = (stock, index[i], data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                 data[11], data[12], data[13])
            c.execute('INSERT INTO hist_datas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', t)

    conn.commit()
    print "Records created successfully"
    conn.close()


def writeDBFromStockHistDatasForUpdateCurrentDay():
    today = time.strftime("%Y-%m-%d")
    writeDBFromStockHistDatasForUpdate(today)


def writeDBFromStockHistDatasForUpdate(today):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()


    stockList = getCandidateFromDB()

    for stock in stockList:
        todayHistData = get_hist_data_by_date(stock, today)
        if len(todayHistData) != 0:
            continue

        data = ts.get_hist_data(stock, start=today, end=today)
        data = data.values

        if len(data) == 0:
            continue

        data = data[0]
        t = (stock, today, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
             data[11], data[12], data[13])

        try:
            c.execute('INSERT INTO hist_datas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', t)
            conn.commit()
        except:
            print 'DB error : failed to insert into hist_datas for stock : ' + str(t)

        print str(stock),

    print "Records update successfully"
    conn.close()


def get_hist_data_by_date(code, date):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (code, date)
    data = []
    rawData = c.execute("select * from hist_datas where code = ? and date = ?", t)
    for row in rawData:
        data.append(row)

    conn.close()
    return data


def writeDBFromTuShare():
    engine = create_engine('sqlite:////Users/chengsilei/PycharmProjects/StockAnalyse/test.db')

    stockList = ts.get_stock_basics()
    stockList.to_sql('stock_basics', engine, if_exists='append')


def readDB():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    data = []
    rawData = c.execute("select * from hist_datas where code = '600570'")
    for row in rawData:
        data.append(row)

    conn.close()


def getCandidateFromDB():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    data = []
    rawData = c.execute("select code from stock_basics")
    for row in rawData:
        data.append(row[0])

    conn.close()
    return data


def get_hist_data(code):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (code,)
    data = []
    rawData = c.execute("select * from hist_datas where code = ? ORDER BY date ASC", t)
    for row in rawData:
        data.append(row)

    conn.close()
    return data


def get_break_through_status(code):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (code,)
    data = []
    rawData = c.execute("select * from break_through where code = ? and status = 0", t)
    for row in rawData:
        data.append(row)

    conn.close()
    return data


def add_new_break_through(code, price, today):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (code, 1, 0, today, -1, '', price, None, None)
    try:
        c.execute('INSERT INTO break_through VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', t)
        conn.commit()
    except:
        print 'DB error : failed to insert into break_throught for stock : ' + str(t)

    conn.close()



def getCandidateFromBreakThoughtStocks():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    data = []
    rawData = c.execute("select code from break_through where direct=1 and status=0")
    for row in rawData:
        data.append(row[0])

    conn.close()
    return data


def update_break_through_for_sell(code, price, today):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (today, price, code)
    try:
        c.execute('update break_through set status = 1, date_sell = ?, price_sell = ? where code = ?', t)
        conn.commit()
    except:
        print 'DB error : failed to update break_through for stock : ' + str(t)

    conn.close()


def add_stock_analyse_data(code, date, m25, m300, N):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (code, date, m25, m300, N)
    c.execute('INSERT INTO analyse_data VALUES (?, ?, ?, ?, ?)', t)

    conn.commit()
    conn.close()


def get_stock_analyse_data(code):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    data = []
    t = (code,)
    rawData = c.execute("select * from analyse_data where code = ? order by date asc", t)
    for row in rawData:
        data.append(row)

    conn.close()
    return data


def add_new_exchange_log(code, price, amt, direct, buyNextPrice=None, buyNextAmt=None, stopPrice=None):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    t = (code, price, amt, direct, buyNextPrice, buyNextAmt, stopPrice, None)
    try:
        c.execute("INSERT INTO exchange_log VALUES (?, datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?)", t)
        conn.commit()
    except:
        print 'DB error : failed to insert into break_throught for stock : ' + str(t)

    conn.close()


def getCurrentlyHoldStocks():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    data = []
    rawData = c.execute("select ba.name, ex.*  \
                          from (SELECT *, MAX(date) \
                            FROM exchange_log \
                            GROUP BY code) ex \
                            join stock_basics ba on ex.code = ba.code\
                            where ex.direct = 1")

    for row in rawData:
        data.append(row)

    conn.close()
    return data


def main():
    #writeDBFromFile()
    #writeDBFromStockHistDatasForUpdate()
    data = getCurrentlyHoldStocks()

    for d in data:
        print str(d)

    #test.f()

if __name__ == '__main__':
    sys.exit(main())