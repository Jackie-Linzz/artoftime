import time
from tornado.concurrent import Future

tables = {}
waiting = {}
desks = set()
desks.add('0001')

class waitingStatus(object):
    def __init__(self):
        self.keep = []
        self.low = -1
        self.high = -1

    def add(self):
        if (self.high + 1) % 100 == self.low:
            return "sorry"
        self.high += 1
        self.keep.append(self.high)
        if len(self.keep) == 1:
            self.low = self.high
        return self.high

    def remove(self, t):
        if t not in self.keep:
            return "sorry"
        self.keep.remove(t)
        if len(self.keep) == 0:
            self.low = -1
            self.high = -1
            return
        if t == self.low:
            while self.low not in self.keep:
                self.low = (self.low + 1) % 100
            return

    def length(self):
        return len(self.keep)


ws = waitingStatus()

class WTable(object):
    def __init__(self, table, number):
        self.table = table
        self.number = number
        self.gdemand = ''
        self.orders = []
        self.waiters = set()
        self.stamp = time.time()

    def to_dict(self):
        result = {'table': self.table, 'number': self.number, 'stamp': self.stamp,
                  'gdemand': self.gdemand,
                  'orders': [one.to_dict() for one in self.orders]}

    def set_future(self):
        for future in self.waiters:
            future.set_result(self.to_dict())
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            future.set_result(self.to_dict())
        else:
            self.waiters.add(future)
        return future
        
######################################################
diet = {}
category = {}
ditem = {'did': '001', 'name': 'coffee', 'price': 25.00, 'price2': 0, 'ord': 1, 'base': 1, 'cid': '001', 'pic': '', 'desp': 'this is coffee'}
diet[ditem['did']] = ditem
citem = {'cid': '001', 'name': 'group1', 'ord': 1, 'desp': 'this is the first group'}
category[citem['cid']] = citem
uid = 0
puid = 0


class Order(object):
    def __init__(self, did, demand=''):
        global diet, uid
        t = diet.get(did)
        if t is None:
            return
        self.did = t['did']
        self.name = t['name']
        self.price = t['price']
        self.price2 = t['price2']
        self.ord = t['ord']
        self.base = t['base']
        self.num = self.base
        self.cid = t['cid']
        self.pic = t['pic']
        self.desp = t['desp']
        self.demand = demand
        
        self.uid = uid
        uid = uid + 1
        self.cook = ''
        self.fb = ''
        self.submit = 0
        self.selected = 0

    def to_dict(self):
        r = {'uid': self.uid, 'did':self.did, 'name': self.name, 'price': self.price,
             'price2': self.price2, 'ord': self.ord, 'base': self.base, 'cid': self.cid,
             'pic': self.pic, 'desp': self.desp, 'demand': self.demand, 'cook': self.cook,
             'fb': self.fb, 'num': self.num}
        return r
        

def waiting_ins(index, ins):
    global waiting
    index = int(index)
    wt = waiting.get(index)
    if not isinstance(wt, WTable):
        return None
    wt.stamp = time.time()
    if ins[0] == '+':
        one = Order(ins[1], ins[2])
        wt.orders.append(one)
    elif ins[0] == '-':
        wt.orders = filter(lambda one: one.uid != ins[1], wt.orders)
    elif ins[0] == 'g':
        wt.gdemand = ins[1]
    wt.set_future()
    return 0

class Table(object):
    def __init__(self, table):
        self.table = table.upper()

        self.gdemand = ''
        self.orders = []
        self.left = []
        
        self.doing = []
        self.done = []
        self.cancel = []

        self.submit = 0
        self.last = 0
        self.stamp = time.time()
        self.waiters = set()
        self.history = []
        
        self.power = 0

    def to_dict(self):
        result = {'table': self.table, 'gdemand': self.gdemand, 'stamp': self.stamp,
                  'orders': [one.to_dict() for one in self.orders],
                  'left': [one.to_dict() for one in self.left],
                  'doing': [one.to_dict() for one in self.doing],
                  'done': [one.to_dict() for one in self.done],
                  'cancel': [one.to_dict() for one in self.cancel]}
        return result

    def set_future(self):
        for future in self.waiters:
            future.set_result(self.to_dict())
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            future.set_result(self.to_dict())
        else:
            self.waiters.add(future)
        return future

    def feedback(self, fb):
        for f in fb:
            for one in self.done:
                if f['uid'] == one.uid:
                    one.fb = f['fb']
    

tables['0001'] = Table('0001')

def customer_ins(table, ins):
    global tables
    table = table.upper()
    table = tables.get(table)
    if not isinstance(table, Table):
        return None
    table.stamp = time.time()
    if ins[0] == '+':
        one = Order(ins[1], ins[2])
        table.orders.append(one)
    elif ins[0] == '-':
        table.orders = filter(lambda one: one.uid != ins[1], table.orders)
    elif ins[0] == 'g':
        table.gdemand = ins[1]
    elif ins[0] == 'submit':
        table.left = table.left + table.orders
        table.orders = []
        table.left = sorted(table.left, key=lambda one: one.ord)
    table.set_future()
    return 0
    
