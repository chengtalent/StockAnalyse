__author__ = 'chengsilei'


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
            if self.data[len(self.data)-i][2] <= self.data[len(self.data)-i][9]:
                self.b = i
                break

    def speak(self):
        print(self.sid + ' : ' + str(self.price) + ' : ' + str(self.b))
        return self.sid + ' : ' + str(self.price) + ' : ' + str(self.b)
