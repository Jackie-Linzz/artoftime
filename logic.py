import time
import os
import mysql
import printer
from tornado.concurrent import Future

data_dir = os.path.expanduser('~/artoftime')
company_file = os.path.expanduser('~/artoftime/company')
data_file = os.path.expanduser('~/artoftime/data')
info = {}
tables = {}
waiting = {}
uids = {}
cooks = {}
desks = set()
diet = {}
category = {}
cook_do = {}
global_uid = 0
global_pid = 0


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


class Order(object):
    def __init__(self, did, desk, demand=''):
        global diet, global_uid
        t = diet.get(did)
        if t is None:
            return
        self.desk = desk
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
        
        self.uid = global_uid
        global_uid += 1
        self.cook = ''
        self.cookname = ''
        self.fb = None
        self.submit = time.time()
        self.inbyway = 0
        
        self.status = 'no' # no, left, doind, done, payed, cash_delete

    def set_left(self):
        global tables
        if self.status == 'left':
            self.inbyway = 0
        elif self.status == 'doing':
            self.inbyway = 0
            self.status = 'left'
            table = tables.get(self.desk)
            table.doing.remove(self)
            table.left.insert(0, self)
        elif self.status == 'done':
            self.inbyway = 0
            self.status = 'left'
            table = tables.get(self.desk)
            table.done.remove(self)
            table.left.insert(0, self)
            
    def set_doing(self):
        global tables
        if self.status == 'left':
            self.inbyway = 0
            self.status = 'doing'
            table = tables.get(self.desk)
            table.left.remove(self)
            table.doing.insert(0, self)
        elif self.status == 'doing':
            pass
        elif self.status == 'done':
            self.inbyway = 0
            self.status = 'doing'
            table = tables.get(self.desk)
            table.done.remove(self)
            table.doing.insert(0, self)
            
    def set_done(self):
        global tables
        if self.status == 'left':
            self.inbyway = 0
            self.status = 'done'
            table = tables.get(self.desk)
            table.left.remove(self)
            table.done.insert(0, self)
        elif self.status == 'doing':
            self.inbyway = 0
            self.status = 'done'
            table = tables.get(self.desk)
            table.doing.remove(self)
            table.done.insert(0, self)

    def cash_delete(self):
        table = tables.get(self.desk)
        table.cash_delete(self)
        if self.inbyway == 1:
            cook = cooks.get(self.cook)
            cook.cash_delete(self)

    def store(self):
        #insert into order_history
        global tables
        mysql.insert('order_history', {'uid': self.uid, 'did': self.did, 'num': self.num, 'price': self.price, 'desk': self.desk,
                                       'pid': tables.get(self.desk).pid, 'stamp': self.submit})
    def to_printer(self):
        content = '%s\t%s\t%s\n' % (self.name, self.num, self.price*self.num)
        result = content.decode('utf-8').encode('gb18030')
        return bytes(result)
            
    def to_dict(self):
        result = {'uid': self.uid, 'did':self.did, 'name': self.name, 'price': self.price,
             'price2': self.price2, 'ord': self.ord, 'base': self.base, 'cid': self.cid,
             'pic': self.pic, 'desp': self.desp, 'demand': self.demand, 'cook': self.cook,
             'cookname': self.cookname, 'fb': self.fb, 'num': self.num}
        return result
        

def waiting_ins(index, ins):
    global waiting, uids
    index = int(index)
    wt = waiting.get(index)
    if not isinstance(wt, WTable):
        return None
    wt.stamp = time.time()
    if ins[0] == '+':
        one = Order(ins[1], index, ins[2])
        wt.orders.append(one)
        uids[one.uid] = one
    elif ins[0] == '-':
        wt.orders = filter(lambda one: one.uid != ins[1], wt.orders)
    elif ins[0] == 'g':
        wt.gdemand = ins[1]
    wt.set_future()
    return 0

class Table(object):
    def __init__(self, table):
        self.table = table.upper()
        self.pid = 0
        self.gdemand = ''
        self.comment = ''
        self.orders = []
        self.left = []
        
        self.doing = []
        self.done = []
        self.cancel = [] #canceled by customer or waiter

        self.payed = []
        self.delete = [] #deleted by cashier

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

    def cash(self, fid):
        self.payed = self.left + self.doing + self.done
        self.orders = []
        self.left = []
        self.doing = []
        self.done = []
        self.cancel = []
        cash_time = time.time()
        for one in self.payed:
            one.status = 'payed'
            one.store()
            mysql.insert('cash_history', {'fid': fid, 'uid': one.uid, 'pid': self.pid, 'status': 'success', 'stamp': cash_time})
            if one.fb is not None:
                mysql.insert('feedback', {'uid': one.uid, 'fb': one.fb, 'stamp': cash_time})
        for one in self.delete:
            one.status = 'delete'
            one.store()
            mysql.insert('cash_history', {'fid': fid, 'uid': one.uid, 'pid': self.pid, 'status': 'failure', 'stamp': cash_time})
        self.delete = []
        self.payed = []
        self.gdemand = ''
        if self.comment != '':
            mysql.insert('comment', {'desk': self.desk, 'comment': self.comment, 'stamp': time.time()})
            self.comment = ''
        #to printer
        printer.gprint(self.to_printer())
        cleanmsg.add(self.desk)

    def to_printer(self):
        global info
        initialization = b'\x1b\x40'
        align_left = b'\x1b\x61\x00'
        align_center = b'\x1b\x61\x01'
        align_right = b'\x1b\x61\x02'
        content = initialization + align_center
        company = info['company'].encode('gb18030')
        content += bytes(company) + b'\n'

        return content
        

    def cash_delete(self, one):
        
        if not isinstance(one, Order):
            return
        if one.status == 'left':
            self.left.remove(one)  
        elif one.status == 'doing':
            self.doing.remove(one)     
        elif one.status == 'done':
            self.done.remove(one)
        self.delete.append(one)
        self.set_future()
        

    def feedback(self, fb):
        for f in fb:
            uid = f['uid']
            one = uids.get(uid)
            if one is None:
                continue
            one.fb = f['fb']


def customer_ins(desk, ins):
    global tables, global_pid, uids
    desk = desk.upper()
    table = tables.get(desk)
    if not isinstance(table, Table):
        return None
    table.stamp = time.time()
    if ins[0] == '+':
        one = Order(ins[1], desk, ins[2])
        if len(table.orders)+len(table.left)+len(table.doing)+len(table.done) == 0:
            table.pid = global_pid
            global_pid += 1
        table.orders.append(one)
        uids[one.uid] = one
        
    elif ins[0] == '-':
        uid = ins[1]
        uid = int(uid)
        one = uids.get(uid)
        if one in table.orders:
            table.orders.remove(one)
            uids.pop(uid)
    elif ins[0] == 'g':
        table.gdemand = ins[1]
    elif ins[0] == 'submit':
        for one in table.orders:
            one.status = 'left'
        table.left = table.left + table.orders
        table.orders = []
        table.left = sorted(table.left, key=lambda one: one.ord)
    table.set_future()
    return 0

def waiter_ins(desk, ins):
    global tables, global_pid, uids
    desk = desk.upper()
    table = tables.get(desk)
    if not isinstance(table, Table):
        return None
    table.stamp = time.time()
    if ins[0] == '+':
        one = Order(ins[1], desk, ins[2])
        if len(table.orders)+len(table.left)+len(table.doing)+len(table.done) == 0:
            table.pid = global_pid
            global_pid += 1
        table.orders.append(one)
        uids[one.uid] = one
    elif ins[0] == '-':
        uid = ins[1]
        one = uids.get(uid)
        if one.status == 'no':
            table.orders.remove(one)
        elif one.status == 'left' and one.inbyway == 0:
            table.left.remove(one)
        uids.pop(uid)
        
    elif ins[0] == 'g':
        table.gdemand = ins[1]
    elif ins[0] == 'submit':
        for one in table.orders:
            one.status = 'left'
        table.left = table.left + table.orders
        table.orders = []
        table.left = sorted(table.left, key=lambda one: one.ord)
    table.set_future()
    return 0
##manager mask update
class Mask(object):
    def __init__(self):
        self.content = set()
        self.stamp = time.time()
        self.waiters = set()
        result = mysql.get_all('mask')
        for one in result:
            self.content.add(one['did'])

    def ins(self, ins):
        if ins[0] == '+':
            did = ins[1]
            if did not in self.content:
                mysql.insert('mask', {'did': did})
                self.content.add(did)
        elif ins[0] == '-':
            did = ins[1]
            if did in self.content:
                mysql.delete('mask', {'did': did})
                self.content.remove(did)
        self.stamp = time.time()
        self.set_future()

    def set_future(self):
        result = self.content
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = self.content
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future

mask = Mask()

class PassMessage(object):
    def __init__(self):
        self.message = set()
        self.stamp = time.time()
        self.waiter = set()

    def add(self, one):
        if not isinstance(one, Order):
            return
        self.message.append(one)
        self.stamp = time.time()
        self.set_future()

    def remove(self, one):
        global uids
        if not isinstance(one, (int, Order)):
            return
        if isinstance(one, int):
            one = uids.get(one)
        self.message.remove(one)
        self.stamp = time.time()
        self.set_future()

    def get_result(self):
        result = [one.to_dict() for one in self.message]
        return result

    def set_future(self):
        result = self.get_result()
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = self.get_result()
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future

passmsg = PassMessage()

class FeedbackMessage(object):
    def __init__(self):
        self.message = set()
        self.stamp = time.time()
        self.waiters = set()

    def add(self, desk):
        self.message.add(desk)
        self.stamp = time.time()
        self.set_future()

    def remove(self, desk):
        self.message.remove(one)
        self.stamp = time.time()
        self.set_future()

    def set_future(self):
        result = list(self.message)
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = list(self.message)
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future

feedbackmsg = FeedbackMessage()
requestmsg = FeedbackMessage()
cleanmsg = FeedbackMessage()

class Cook(object):
    def __init__(self, fid):
        self.fid = fid
        self.name = fids.get(fid)['name']
        self.current = None
        self.byway = []
        self.doing = []
        self.done = []
        self.deny = []
        self.cookdo = []
        self.waiters = set()
        self.stamp = time.time()
        self.queue = []

    def ins(self, ins):
        #ins: accept,refuse,cancel-byway,cancel-doing,done
        global uids
        if ins[0] == 'accept':
            if self.current is None:
                self.current = self.select()
                self.select_byway()
               
            else:
                items = ins[1:]
                for uid in items:
                    uid = int(uid)
                    one = uids.get(uid)
                    one.cook = self.fid
                    one.cookname = self.name
                    one.set_doing()
                    self.doing.append(one)
                self.byway = []
                self.deny = []
                self.current = None
                
        elif ins[0] == 'refuse':
            if self.current is None:
                pass
            else:
                did = self.current.did
                self.deny.append(did)
        elif ins[0] == 'cancel-byway':
            uid = ins[1]
            one = uids.get(uid)
            self.byway.remove(one)
            one.set_left()
        elif ins[0] == 'cancel-doing':
            uid = ins[1]
            one = uids.get(uid)
            self.doing.remove(one)
            one.set_left()
        elif ins[0] == 'done':
            uid = ins[1]
            uid = int(uid)
            one = uids.get(uid)
            self.doing.remove(one)
            self.done.append(one)
            one.set_done()
            #store into cook_history
            mysql.insert('cook_history', {'fid': self.fid, 'uid': uid, 'stamp': time.time()})
            #insert pass message
            passmsg.add(one)
            #check feedback request
            table = tables.get(one.desk)
            if len(table.left)+len(table.doing) == 0:
                feedbackmsg.add(one.desk)
        self.stamp = time.time()
        self.set_future()
        
    def select(self):
        # when selecting, consider cookdo and deny
        global tables
        current = time.time()
        left = filter(lambda x: len(x.left)>0, tables.values())
        for table in left:
            table.power = (current-table.submit)*0.15+(current-table.last)*0.85
        left.sort(key=lambda x: x.power)
        self.queue = left
        if len(left) == 0:
            return None
        else:
            # select not in byway
            for table in left:
                for one in table.left:
                    if one.did in self.cookdo and one.did not in self.deny and one.inbyway == 0:
                        one.inbyway = 1
                        one.cook = self.fid
                        return one            
            return None

    def select_byway(self):
        global tables
        self.byway = []
        if self.current is None:
            return
        did = self.current.did
        for table in self.queue:
            for one in table.left:
                if one.did == did and one.inbyway == 0:
                    one.inbyway = 1
                    self.byway.append(one)
                    one.cook = self.fid
                    if len(self.byway) >= 5:
                        return

    def cash_delete(self, one):
        if not isinstance(one, Order):
            return
        if one.status == 'left':
            if self.current == one:
                self.current = None
            elif one in self.byway:
                self.byway.remove(one)
            one.inbyway = 0
        elif one.status == 'doing':
            self.doing.remove(one)
        elif one.status == 'done':
            self.done.remove(one)
        self.set_future()
            

    def to_dict(self):
        if self.current is None:
            cur = ''
        else:
            cur = self.current.to_dict()
        result = {'fid': self.fid, 'name': self.name, 'current': cur, 'stamp': self.stamp,
                  'byway': [one.to_dict() for one in self.byway],
                  'doing': [one.to_dict() for one in self.doing],
                  'done': [one.to_dict() for one in self.done]}
        return result

    def set_future(self):
        result = self.to_dict()
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = self.to_dict()
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future
    
        
        
