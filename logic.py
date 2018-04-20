#coding=utf8
import time
import os
import platform
import mysql
import printer

from tornado.concurrent import Future

data_dir = os.path.expanduser('~/data')
company_file = os.path.expanduser('~/data/company')
data_file = os.path.expanduser('~/data/data')
if platform.system() == 'Linux':
    data_dir = '/home/jerry/data'
    company_file = '/home/jerry/data/company'
    data_file = '/home/jerry/data/data'

info = {}
tables = {}

uids = {}
faculty = {}
working_cooks = set()

cooks = {}
waiters = {}
desks = set()
diet = {}
category = {}
cook_do = {} #fid: set()
global_uid = 0
global_pid = 0

queue_cursor = 1



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

class Queue(object):
    def __init__(self):
        self.queue = []
        self.waiters = set()
        self.stamp = time.time()

    def add(self, number):
        global queue_cursor
        item = {'order': queue_cursor, 'num': number}
        queue_cursor += 1
        self.queue.append(item)
        self.set_future()

    def remove(self, order):
        self.queue = filter(lambda x: x['order'] != order, self.queue)
        self.set_future()
        
    def set_future(self):
        self.stamp = time.time()
        result = self.queue
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = self.queue
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future
queue = Queue()

class Idle_desks(object):
    def __init__(self):
        self.desks = []
        self.waiters = set()
        self.stamp = time.time()
        self.init()

    def init(self):
        #import pdb
        #pdb.set_trace()
        global tables
        self.desks = []
        for k, v in tables.items():
            if len(v.left)+len(v.doing)+len(v.done) == 0:
                self.desks.append({'desk': k, 'num': v.seats})
        self.desks.sort(key=lambda x: x['num'])

    def add(self, desk):
        self.desks.append({'desk': desk, 'num': tables[desk].seats})
        self.desks.sort(key=lambda x: x['num'])
        self.set_future()

    def remove(self, desk):
        self.desks = filter(lambda x: x['desk'] != desk, self.desks)
        self.set_future()

    def set_future(self):
        self.stamp = time.time()
        result = self.desks
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = self.desks
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future

idle_desks = Idle_desks()
        
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
        
        self.status = 'no' # no, left, doing, done, payed, cash_delete
        self.passed = 0

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
            #table.stamp = time.time()
            table.set_future()
        elif self.status == 'done':
            self.status = 'left'
            table = tables.get(self.desk)
            table.done.remove(self)
            table.left.insert(0, self)
            #table.stamp = time.time()
            table.set_future()
            
    def set_doing(self):
        global tables
        self.inbyway = 0
        if self.status == 'left':
            self.status = 'doing'
            table = tables.get(self.desk)
            table.left.remove(self)
            table.doing.insert(0, self)
            #table.stamp = time.time()
            table.set_future()
        elif self.status == 'doing':
            pass
        elif self.status == 'done':
            self.inbyway = 0
            self.status = 'doing'
            table = tables.get(self.desk)
            table.done.remove(self)
            table.doing.insert(0, self)
            #table.stamp = time.time()
            table.set_future()
            
    def set_done(self):
        global tables
        self.inbyway = 0
        if self.status == 'left':
            self.status = 'done'
            table = tables.get(self.desk)
            table.left.remove(self)
            table.done.insert(0, self)
            #table.stamp = time.time()
            table.set_future()
        elif self.status == 'doing':
            self.status = 'done'
            table = tables.get(self.desk)
            table.doing.remove(self)
            table.done.insert(0, self)
            #table.stamp = time.time()
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
        #align_left = b'\x1b\x61\x00'
        content = u'%s\t%s\t%s\n' % (self.name, self.num, self.price*self.num)
        result = bytes(content.encode('gb18030'))
        return result
            
    def to_dict(self):
        result = {'uid': self.uid, 'did':self.did, 'name': self.name, 'desk': self.desk, 'price': self.price,
                  'price2': self.price2, 'ord': self.ord, 'base': self.base, 'cid': self.cid, 'gdemand': tables.get(self.desk).gdemand,
                  'pic': self.pic, 'desp': self.desp, 'demand': self.demand, 'cook': self.cook,
                  'cookname': self.cookname, 'fb': self.fb, 'num': self.num}
        return result
        



class Table(object):
    def __init__(self, table):
        self.table = table.upper()
        self.seats = mysql.get('desks', {'desk': table})[0]['num']
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
        self.stamp = time.time()
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
        printer.gprint(self.to_printer())
        self.delete = []
        self.payed = []
        self.gdemand = ''
        if self.comment != '':
            mysql.insert('comment', {'desk': self.table, 'comment': self.comment, 'stamp': time.time()})
            self.comment = ''
        cleanmsg.add(self.table)
        feedbackmsg.remove(self.table)
        #requestmsg.remove(self.table)
        idle_desks.add(self.table)
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
        content += b'\n\n\n\n\n'
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

def get_ordernum_waiter():
    num = 0
    for table in tables.values():
        for one in table.left:
            if one.who == 'waiter':
                num += 1
    return num

def customer_ins(desk, ins):
    global tables, global_pid, uids, idle_desks
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
            if one.who == 'waiter':
                num = get_ordernum_waiter()
                statusmsg.change(receive=num)                
        
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
        idle_desks.remove(desk)
    table.set_future()
    return 0

def waiter_ins(desk, ins):
    global tables, global_pid, uids, idle_desks
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
            if one.who == 'waiter':
                num = get_ordernum_waiter()
                statusmsg.change(receive=num) 
            
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
        idle_desks.remove(desk)
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
        self.stamp = time.time()
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
        self.stamp = time.time()
        result = self.get_result()
        statusmsg.change(passl=len(result))
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
        self.stamp = time.time()
        result = list(self.message)
        statusmsg.change(feedback=len(result))
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

class RequestMessage(object):
    def __init__(self):
        self.message = set()
        self.stamp = time.time()
        self.waiters = set()

    def add(self, desk):
        self.message.add(desk)
        mysql.insert('request', {'desk': desk, 'stamp': time.time()})
        self.stamp = time.time()
        self.set_future()

    def remove(self, desk):
        if desk in self.message:
            self.message.remove(desk)
        self.stamp = time.time()
        self.set_future()

    def set_future(self):
        self.stamp = time.time()
        result = list(self.message)
        statusmsg.change(request=len(result))
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
    
requestmsg = RequestMessage()

class CleanMessage(object):
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
        self.stamp = time.time()
        result = list(self.message)
        statusmsg.change(clean=len(result))
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

cleanmsg = CleanMessage()
#for all orders in table.left
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
            for one in v.left:
                if one.who == 'cook':
                    left += one.num
        self.num = left
        return left
    
    def set_future(self):
        self.stamp = time.time()
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
#for orders for waiters in table.left
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
        self.stamp = time.time()
        result = self.get_result()
        statusmsg.change(receive=len(result))
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

class Status(object):
    def __init__(self):
        self.message = {'receive': 0, 'pass': 0, 'request': 0, 'feedback': 0, 'clean': 0}
        self.stamp = time.time()
        self.waiters = set()

    def change(self, receive=0, passl=0, request=0, feedback=0, clean=0):
        
        self.set_future()

    def get_result(self):
        receive = get_ordernum_waiter()
        passl = len(passmsg.message)
        request = len(requestmsg.message)
        feedback = len(feedbackmsg.message)
        clean = len(cleanmsg.message)
        self.message = {'receive': receive, 'pass': passl, 'request': request, 'feedback': feedback, 'clean': clean}
    def set_future(self):
        self.stamp = time.time()
        self.get_result()
        result = self.message
        for future in self.waiters:
            future.set_result(result)
        self.waiters = set()

    def update(self, stamp):
        future = Future()
        if stamp < self.stamp:
            result = self.message
            future.set_result(result)
        else:
            self.waiters.add(future)
        return future

statusmsg = Status()

class Cook(object):
    def __init__(self, fid):
        self.fid = fid
        self.name = faculty.get(fid)['name']
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
        print ins
        if ins[0] == 'prepare':
            if self.current is None:
                self.current = self.select()
                self.select_byway()
        if ins[0] == 'accept':
            if self.current is None:
                pass               
            else:
                
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
            uid = int(uid)
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
            items = ins[1:]
            for uid in items:
                uid = int(uid)
                one = uids.get(uid)
                if one in self.doing:
                    self.doing.remove(one)
                    self.done.insert(0, one)
                    if len(self.done) > 50:
                        self.done = self.done[0:49]
                    one.set_done()
                    #store into cook_history
                    mysql.insert('cook_history', {'fid': self.fid, 'uid': uid, 'stamp': time.time()})
                    #insert pass message
                    passmsg.add(one)
                    #check feedback request
                    table = tables.get(one.desk)
                    table.last = time.time()
                    if len(table.left)+len(table.doing) == 0:
                        feedbackmsg.add(one.desk)
        elif ins[0] == 'done-all':
            for one in self.doing:    
                self.done.insert(0, one)
                if len(self.done) > 50:
                    self.done = self.done[0:49]
                one.set_done()
                #store into cook_history
                mysql.insert('cook_history', {'fid': self.fid, 'uid': one.uid, 'stamp': time.time()})
                #insert pass message
                passmsg.add(one)
                #check feedback request
                table = tables.get(one.desk)
                table.last = time.time()
                if len(table.left)+len(table.doing) == 0:
                    feedbackmsg.add(one.desk)
            self.doing = []
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
                    if len(self.byway) >= 2:
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
        self.stamp = time.time()
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
        self.name = faculty.get(fid)['name']
        self.done = []
        self.passed = []
        self.waiters = set()
        self.stamp = time.time()

    def to_dict(self):
        result = {'fid': self.fid, 'name': self.name, 'done': [one.to_dict() for one in self.done],
                  'passed': [one.to_dict() for one in self.passed]}
        return result

    def receive(self, uid):
        global uids
        uid = int(uid)
        one = uids.get(uid)
        if one is None:
            return
        if one.status == 'left':
            self.done.insert(0, one)
            self.done = self.done[0:50]
            one.set_done()
            one.cook = self.fid
            one.cookname = self.name
            table = tables.get(one.desk)
            if len(table.left) + len(table.doing) == 0:
                feedbackmsg.add(one.desk)
            mysql.insert('waiter_receive_history', {'fid': self.fid, 'uid': uid, 'stamp': time.time()})
            one.passed = 1
            self.passed.insert(0, one)
            self.passed = self.passed[0:50]
            left2msg.change()
            self.set_future()
    def passl(self, uid):
        global uids
        uid = int(uid)
        one = uids.get(uid)
        if one is None:
            return
        if one.passed == 0:
            one.passed = 1
            self.passed.insert(0, one)
            self.passed = self.passed[0:50]
            self.set_future()

    def set_future(self):
        self.stamp = time.time()
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

