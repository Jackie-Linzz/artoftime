#coding=utf8
import time
import os
import mysql
import printer
from tornado.concurrent import Future

data_dir = os.path.expanduser('~/data')
company_file = os.path.expanduser('~/data/company')
data_file = os.path.expanduser('~/data/data')
info = {}
tables = {}
waiting = {}
uids = {}
cooks = {}
waiters = {}
desks = set()
diet = {}
category = {}
cook_do = {} #fid: set()
global_uid = 0
global_pid = 0



def add_uid():
    global global_uid
    global_uid += 1
    sql = 'update id set num = %s where name = "uid"' % global_uid
    mysql.execute(sql)

def add_pid():
    global global_pid
    global_pid += 1
    sql = 'update id set num = %s where name = "pid"' % global_pid
    mysql.execute(sql)

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
        global diet, global_uid, add_uid
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
        self.who = t['who']
        self.pic = t['pic']
        self.desp = t['desp']
        self.demand = demand
        
        self.uid = global_uid
        #print 'global_uid:',global_uid
        add_uid()
        self.cook = None
        self.cookname = None
        self.fb = None
        self.submit = time.time()
        self.inbyway = 0
        
        self.status = 'no' # no, left, doind, done, payed, cash_delete

    def set_left(self):
        global tables
        self.cook = None
        self.cookname = None
        self.inbyway = 0
        if self.status == 'left':
            pass
        elif self.status == 'doing':
            self.status = 'left'
            table = tables.get(self.desk)
            table.doing.remove(self)
            table.left.insert(0, self)
            table.set_future()
        elif self.status == 'done':
            self.status = 'left'
            table = tables.get(self.desk)
            table.done.remove(self)
            table.left.insert(0, self)
            table.set_future()
            
    def set_doing(self):
        global tables
        self.inbyway = 0
        if self.status == 'left':
            self.status = 'doing'
            table = tables.get(self.desk)
            table.left.remove(self)
            table.doing.insert(0, self)
            table.set_future()
        elif self.status == 'doing':
            pass
        elif self.status == 'done':
            self.inbyway = 0
            self.status = 'doing'
            table = tables.get(self.desk)
            table.done.remove(self)
            table.doing.insert(0, self)
            table.set_future()
            
    def set_done(self):
        global tables
        self.inbyway = 0
        if self.status == 'left':
            self.status = 'done'
            table = tables.get(self.desk)
            table.left.remove(self)
            table.done.insert(0, self)
            table.set_future()
        elif self.status == 'doing':
            self.status = 'done'
            table = tables.get(self.desk)
            table.doing.remove(self)
            table.done.insert(0, self)
            table.set_future()

    def cash_delete(self):
        if self.status == 'left':
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
        align_left = b'\x1b\x61\x00'
        content = u'%s\t%s\t%s\n' % (self.name, self.num, self.price*self.num)
        result = align_left + bytes(content.encode('gb18030'))
        return result
            
    def to_dict(self):
        result = {'uid': self.uid, 'did':self.did, 'name': self.name, 'desk': self.desk, 'price': self.price,
                  'price2': self.price2, 'ord': self.ord, 'base': self.base, 'cid': self.cid, 'gdemand': tables.get(self.desk).gdemand,
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
        if len(self.left)+len(self.doing) >0:
            return 'failure'
        if len(self.done) == 0:
            return 'failure'
        self.payed = self.done
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
        # to gprinter
        #printer.gprint(self.to_printer())
        self.delete = []
        self.payed = []
        self.gdemand = ''
        if self.comment != '':
            mysql.insert('comment', {'desk': self.table, 'comment': self.comment, 'stamp': time.time()})
            self.comment = ''
        cleanmsg.add(self.table)
        feedbackmsg.remove(self.table)
        #requestmsg.remove(self.table)
        return 'success'

    def to_printer(self):
        global info
        initialization = b'\x1b\x40'
        align_left = b'\x1b\x61\x00'
        align_center = b'\x1b\x61\x01'
        align_right = b'\x1b\x61\x02'
        content = initialization + align_center
        company = info['company'].encode('gb18030')
        content += bytes(company) + b'\n\n'
        content += bytes(unicode(self.pid).encode('gb18030')) + b'\n\n'
        times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        times += '\n'
        content += align_right
        content += bytes(times.encode('gb18030'))
        content += bytes((u'-'*32+u'\n').encode('gb18030'))
        content += align_left
        content += bytes(('%s\t%s\t%s\n' % (u'名称',u'数量',u'价格')).encode('gb18030'))
        all = 0
        for one in self.payed:
            all += one.price*one.num
            content += one.to_printer()
        content += bytes((u'-'*32+u'\n').encode('gb18030'))
        #content += align_right
        content += bytes((u'共\t\t%s'% all).encode('gb18030'))
        content += b'\n\n\n\n\n\n'
        return content
        

    def cash_delete(self, one):
        
        if not isinstance(one, Order):
            return
        if one.status == 'left':
            self.left.remove(one)
            
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
        if ins[1] not in diet:
            return
        did = ins[1]
        demand = ins[2]
        flag = False
        for one in table.orders:
            if one.did == did and one.demand == demand and one.inbyway == 0:
                one.num += one.base
                flag = True
                break
        if flag == False:
            one = Order(did, desk, demand)
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
        if len(table.left)+len(table.doing)+len(table.done) == 0:
            table.submit = time.time()
            table.pid = global_pid
            add_pid()
        for one in table.orders:
            one.status = 'left'
        table.left = table.left + table.orders
        table.orders = []
        table.left = sorted(table.left, key=lambda one: one.ord)
        leftmsg.change()
        left2msg.change()
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
        if ins[1] not in diet:
            return
        did = ins[1]
        demand = ins[2]
        flag = False
        for one in table.orders:
            if one.did == did and one.demand == demand and one.inbyway == 0:
                one.num += one.base
                flag = True
                break
        if flag == False:
            one = Order(did, desk, demand)
            table.orders.append(one)
            uids[one.uid] = one
            
    elif ins[0] == '-':
        uid = ins[1]
        one = uids.get(uid)
        if one.status == 'no':
            table.orders.remove(one)
            uids.pop(uid)
        elif one.status == 'left':
            if one.inbyway == 0:
                table.left.remove(one)
            else:
                fid = one.cook
                cook = cooks.get(fid)
                cook.ins(['remove', one.uid])
                table.left.remove(one)
            leftmsg.change()
            uids.pop(uid)
        
        
    elif ins[0] == 'g':
        table.gdemand = ins[1]
    elif ins[0] == 'submit':
        if len(table.left)+len(table.doing)+len(table.done) == 0:
            table.submit = time.time()
            table.pid = global_pid
            add_pid()
        for one in table.orders:
            one.status = 'left'
        table.left = table.left + table.orders
        table.orders = []
        table.left = sorted(table.left, key=lambda one: one.ord)
        leftmsg.change()
        left2msg.change()
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
                result = mysql.insert('mask', {'did': did})
                if result:
                    self.content.add(did)
        elif ins[0] == '-':
            did = ins[1]
            if did in self.content:
                result = mysql.delete('mask', {'did': did})
                if result:
                    self.content.remove(did)
        self.stamp = time.time()
        self.set_future()

    def get_result(self):
        result = []
        for one in self.content:
            result.append({'did': one, 'name': diet.get(one)['name'], 'cid': diet.get(one)['cid']})
        result.sort(key=lambda x: x['did'])
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

mask = Mask()
#print 'mask:',mask.content

class PassMessage(object):
    def __init__(self):
        self.message = set()
        self.stamp = time.time()
        self.waiters = set()

    def add(self, one):
        if not isinstance(one, Order):
            return
        self.message.add(one)
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
        if desk in self.message:
            self.message.remove(desk)
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

class LeftMessage(object):
    def __init__(self):
        self.num = 0
        self.stamp = time.time()
        self.waiters = set()

    def change(self):
        self.stamp = time.time()
        self.set_future()

    def get_result(self):
        global tables
        left = 0
        for v in tables.values():
            left += len(v.left)
        self.num = left
        return left
    
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

leftmsg = LeftMessage()

class Left2Message(object):
    def __init__(self):
        self.content = []
        self.stamp = time.time()
        self.waiters = set()

    def change(self):
        self.stamp = time.time()
        self.set_future()

    def get_result(self):
        global tables
        result = []
        for v in tables.values():
            for one in v.left:
                if one.who == 'waiter':
                    result.append(one)
        
        return [one.to_dict() for one in result]
    
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

left2msg = Left2Message()

class Cook(object):
    def __init__(self, fid):
        self.fid = fid
        self.name = mysql.get('faculty', {'fid': fid})[0]['name']
        self.current = None
        self.byway = []
        self.doing = []
        self.done = []
        #self.deny = []
        self.cookdo = []
        self.waiters = set()
        self.stamp = time.time()
        self.queue = []
        #init self.cookdo
        result = mysql.get('cook_do', {'fid': self.fid})
        all = False
        for one in result:
            if one['did'] == 'all':
                all = True
            self.cookdo.append(one['did'])
        if all:
            self.cookdo = ['all']

    def ins(self, ins):#waiter-ins remove one when one in byway
        #ins: accept,refuse,cancel-byway,cancel-doing,done
        global uids
        if ins[0] == 'prepare':
            if self.current is None:
                self.current = self.select()
                self.select_byway()
        if ins[0] == 'accept':
            if self.current is None:
                pass               
            else:
                items = ins[1:]
                items = []
                items.append(self.current.uid)
                for one in self.byway:
                    items.append(one.uid)
                for uid in items:
                    uid = int(uid)
                    one = uids.get(uid)
                    if one is not None:
                        one.cook = self.fid
                        one.cookname = self.name
                        one.inbyway = 0
                        one.set_doing()
                        self.doing.append(one)
                        if one in self.byway:
                            self.byway.remove(one)
                for one in self.byway:
                    one.inbyway = 0
                    one.cook = None
                    one.cookname = None
                leftmsg.change()
                self.byway = []
                #self.deny = []
                self.current = None
                
        elif ins[0] == 'refuse':
            if self.current is None:
                pass
            else:
                #did = self.current.did
                #self.deny.append(did)
                self.current.cook = None
                self.current.cookname = None
                self.current.inbyway = 0
                self.current = None
                for one in self.byway:
                    one.cook = None
                    one.cookname = None
                    one.inbyway = 0
                self.byway = []
        elif ins[0] == 'remove':
            one = uids.get(ins[1])
            if one in self.byway:
                one.cook = None
                one.cookname = None
                one.inbyway = 0
                self.byway.remove(one)
            if one is self.current:
                self.current.cook = None
                self.current.cookname = None
                self.current.inbyway = 0
                self.current = None
                for one in self.byway:
                    one.cook = None
                    one.cookname = None
                    one.inbyway = 0
                self.byway = []
                
        elif ins[0] == 'cancel-byway':
            uid = ins[1]
            one = uids.get(uid)
            if one in self.byway:
                self.byway.remove(one)
                one.set_left()
        elif ins[0] == 'cancel-doing':
            uid = ins[1]
            one = uids.get(uid)
            if one in self.doing:
                self.doing.remove(one)
                one.set_left()
                leftmsg.change()
        elif ins[0] == 'done':
            uid = ins[1]
            uid = int(uid)
            one = uids.get(uid)
            if one in self.doing:
                self.doing.remove(one)
                self.done.insert(0, one)
                if len(self.done) > 50:
                    self.done = self.done[0:49]
                one.set_done()
                tables.get(one.desk).last = time.time()
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
        #import pdb
        #pdb.set_trace()
        left = filter(lambda x: len(x.left)>0, tables.values())
        for table in left:
            table.power = (current-table.submit)*0.15+(current-table.last)*0.85
        left.sort(key=lambda x: x.power, reverse=True)
        self.queue = left
        
        if len(left) == 0:
            return None
        else:
            # select not in byway
            for table in left:
                for one in table.left:
                    if one.who == 'cook' and one.inbyway == 0:
                        if 'all' in self.cookdo or one.did in self.cookdo:
                            one.inbyway = 1
                            one.cook = self.fid
                            one.cookname = self.name
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
                    one.cookname = self.name
                    if len(self.byway) > 3:
                        return

    def cash_delete(self, one):
        if not isinstance(one, Order):
            return
        if one.status == 'left' and one.inbyway ==1:
            self.ins(['remove', one.uid])

    def to_dict(self):
        if self.current is None:
            cur = ''
        else:
            cur = self.current.to_dict()
        result = {'fid': self.fid, 'name': self.name, 'current': cur, 'stamp': self.stamp, 'cookdo': self.cookdo,
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
    
class Waiter(object):
    def __init__(self, fid):
        self.fid = fid
        self.name = mysql.get('faculty', {'fid': fid})[0]['name']
        self.done = []
        self.waiters = set()
        self.stamp = time.time()

    def to_dict(self):
        result = {'fid': self.fid, 'name': self.name, 'done': [one.to_dict() for one in self.done]}
        return result

    def receive(self, uid):
        global uids
        one = uids.get(uid)
        if one is None:
            return
        self.stamp = time.time()
        self.done.insert(0, one)
        self.done = self.done[0:50]
        one.set_done()
        mysql.insert('cook_history', {'fid': self.fid, 'uid': uid, 'stamp': time.time()})
        left2msg.change()
        self.set_future()

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

