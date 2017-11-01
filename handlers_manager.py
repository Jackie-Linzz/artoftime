import tornado.web
import pickle
import datetime
import time
import logic
import mysql
import os
import qrcode
import MySQLdb

from tornado.escape import json_encode, json_decode

class ManagerHomeHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-home.html')

class ManagerCompanyHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-company.html')

    def post(self):
        file = logic.company_file
        with open(file, 'rb') as f:
            info = pickle.load(f)
        response = {'info': info}
        self.write(json_encode(response))

class ManagerCompanySetHandler(tornado.web.RequestHandler):
    def post(self):
        company = self.get_argument('company')
        shop = self.get_argument('shop')
        location = self.get_argument('location')
        heading = self.get_argument('heading')
        welcome = self.get_argument('welcome')
        desp = self.get_argument('desp')
        info = {'company': company, 'shop': shop, 'location': location, 'heading': heading, 'welcome': welcome, 'desp': desp}
        file = logic.company_file
        with open(file, 'wb') as f:
            pickle.dump(info, f)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class ManagerDietHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-diet.html')
        
class ManagerGroupAddHandler(tornado.web.RequestHandler):
    def post(self):
        cid = self.get_argument('cid')
        cname = self.get_argument('cname')
        corder = self.get_argument('corder')
        cdesp = self.get_argument('cdesp')
        corder = int(corder)
        result = mysql.insert('category', {'cid':cid, 'name': cname, 'ord': corder, 'desp': cdesp})
        if result:
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerGroupDelHandler(tornado.web.RequestHandler):
    def post(self):
        cid = self.get_argument('cid')
        result = mysql.delete('category', {'cid': cid})
        if result:
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerGroupShowHandler(tornado.web.RequestHandler):
    def post(self):
        result = mysql.get_all('category')
        result.sort(key=lambda one: one['cid'])
        response = {'status': 'ok', 'category': result}
        self.write(json_encode(response))

class ManagerDietAddHandler(tornado.web.RequestHandler):
    def post(self):
        did = self.get_argument('did')
        name = self.get_argument('name')
        order = self.get_argument('order')
        price = self.get_argument('price')
        price2 = self.get_argument('price2')
        base = self.get_argument('base')
        cid = self.get_argument('cid')
        desp = self.get_argument('desp')
        
        order = int(order)
        price = float(price)
        price2 = float(price2)
        base = float(base)
        picture = ''
        
        if self.request.files:
            metas = self.request.files['picture']
            for meta in metas:
                file_name = meta['filename']
                content = meta['body']
                ext = os.path.splitext(file_name)[-1]
                picture = str(did) + ext
                full_path = os.path.join(os.getcwd(), 'static/pictures/' + picture)
                with open(full_path, 'wb') as f:
                    f.write(content)
        result = mysql.insert('diet', {'did': did, 'name': name, 'ord': order, 'price': price, 'price2': price2, 'base': base, 'cid': cid, 'desp': desp, 'pic': picture})
        if result:
            response = {'status': 'ok'}
        else:
            os.remove(os.path.join(os.getcwd(), 'static/pictures/' + picture))
            response = {'status': 'error'}
        self.write(response)

class ManagerDietDelHandler(tornado.web.RequestHandler):
    def post(self):
        did = self.get_argument('did')
        result = mysql.get('diet', {'did': did})
        if result and result[0]:
            picture = result[0]['pic']
            full_path = os.path.join(os.getcwd(), 'static/pictures/' + picture)
            
            if mysql.delete('diet', {'did': did}) and picture != '':
                os.remove(full_path)
            response = {'status': 'ok'}
            self.finish(json_encode(response))
            return
        response = {'status': 'error'}
        self.finish(json_encode(response))

class ManagerDietShowHandler(tornado.web.RequestHandler):
    def post(self):
        result = mysql.get_all('diet');
        result.sort(key=lambda one: one['cid'])
        response = {'status': 'ok', 'diet': result}
        self.write(json_encode(response))

class ManagerDeskHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-desk.html')

class ManagerDeskAddHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        result = mysql.insert('desks', {'desk': desk})
        if result:
            path = os.path.join(os.getcwd(), 'static/desks/' + desk)
            data = desk
            img = qrcode.make(data)
            img.save(path)
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerDeskDelHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        result = mysql.delete('desks', {'desk': desk})
        if result:
            path = os.path.join(os.getcwd(), 'static/desks/' + desk)
            os.remove(path)
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerDeskShowHandler(tornado.web.RequestHandler):
    def post(self):
        desks = mysql.get_all('desks')
        desks.sort()
        response = {'status': 'ok', 'desks': desks}
        self.write(json_encode(response))

class ManagerWorkerHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-worker.html')

class ManagerWorkerAddHandler(tornado.web.RequestHandler):
    def post(self):
        fid = self.get_argument('fid')
        name = self.get_argument('name')
        passwd = self.get_argument('passwd')
        role = json_decode(self.get_argument('role'))
        role = ','.join(role)
        result = mysql.insert('faculty', {'fid': fid, 'name': name, 'role': role})
        result2 = mysql.insert('password', {'fid': fid, 'passwd': passwd})
        if result and result2:
            response = {'status': 'ok'}
        else:
            mysql.delete('faculty', {'fid': fid})
            mysql.delete('password', {'fid': fid})
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerWorkerDelHandler(tornado.web.RequestHandler):
    def post(self):
        fid = self.get_argument('fid')
        result = mysql.delete('faculty', {'fid': fid})
        result2 = mysql.delete('password', {'fid': fid})
        if result and result2:
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerWorkerShowHandler(tornado.web.RequestHandler):
    def post(self):
        sql = 'select faculty.fid, name, role, passwd from faculty, password where faculty.fid = password.fid'
        result = mysql.query(sql)
        response = {'status': 'ok', 'workers': result}
        self.write(json_encode(response))

class ManagerCookdoHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-cookdo.html')

    def post(self):
        fid = self.get_argument('fid')
        sql = 'select did from cook_do where fid = "%s"' % fid
        #sql = 'select diet.did, name, cid from cookdo, diet where fid = "%s" and cookdo.did = diet.did' % fid
        result = mysql.query(sql)
        if len(result) == 0:
            return
        all = False
        for one in result:
            if one['did'] == all:
                all = True
                break
        if all:
            response = {'status': 'ok', 'result': 'all'}
        else:
            sql = 'select diet.did, name, cid from cook_do, diet where fid = "%s" and cook_do.did = diet.did' % fid
            cookdo = mysql.query(sql)
            response = {'status': 'ok', 'result': 'some', 'cookdo': cookdo}
        self.write(json_encode(response))
        
class ManagerAchievementHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-achievement.html')

    def post(self):
        t1 = self.get_argument('from')
        t2 = self.get_argument('to')
        fid = self.get_argument('fid')
        format = '%Y-%m-%d'
        t1 = datetime.datetime.strptime(t1, format)
        t2 = datetime.datetime.strptime(t2, format)
        if t1 >= t2:
            return
        sql = 'select role from faculty where fid = "%s" ' % fid
        result = mysql.query(sql)
        if result is None or len(result) == 0:
            return
        roles = result[0]['role']
        roles = roles.split(',')
        response = {'status': 'ok', 'roles': roles}

        t1 = time.mktime(t1.timetuple())
        t2 = time.mktime(t2.timetuple())
        if 'cashier' in roles:
            sql = 'select count(*) as number from cash_history where status = "success" and stamp > %s and stamp < %s ' % (t1, t2)
            result = mysql.query(sql)
            success = result[0]['number']
            sql = 'select count(*) as number from cash_history where status = "failure" and stamp > %s and stamp < %s ' % (t1, t2)
            result = mysql.query(sql)
            failure = result[0]['number']
            response['cashier'] = {'success': success, 'failure': failure}
        if 'cook' in roles:
            sql = 'select name, sum(num) as number from diet,order_history,cook_history where diet.did = order_history.did and order_history.uid = cook_history.uid and fid = "%s" and cook_history.stamp > %s and cook_history.stamp < %s group by name' % (fid, t1, t2)
            result = mysql.query(sql)
            response['flow'] = result
            sql = 'select name, sum(num) as number, fb from diet,order_history,cook_history,feedback where diet.did = order_history.did and order_history.uid = cook_history.uid and cook_history.uid = feedback.uid and fid = "%s" and cook_history.stamp > %s and cook_history.stamp < %s group by name,fb' % (fid, t1, t2)
            result = mysql.query(sql)
            fb = []
            temp = {}
            for one in result:
                name = one['name']
                number = one['number']
                if one['fb'] == -1:
                    temp[name]['bad'] = number
                elif one['fb'] == 0:
                    temp[name]['normal'] = number
                else:
                    temp[name]['good'] = number
            for k, v in temp.items():
                total = v['good'] + v['normal'] + v['bad']
                if total == 0:
                    fb.append({'name': k, 'good': v['good'], 'normal': v['normal'], 'bad': v['bad'], 'goodrate': '0%', 'badrate': '0%'})
                else:
                    total = float(total)
                    rate1 = v['good'] * 100 / total
                    rate2 = v['bad'] * 100 / total
                    fb.append({'name': k, 'good': v['good'], 'normal': v['normal'], 'bad': v['bad'], 'goodrate': str(rate1)+'%', 'badrate': str(rate2)+'%'})
            response['fb'] = fb
        self.write(json_encode(response))

class ManagerHistoryHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-history.html')

class ManagerHistoryFlowHandler(tornado.web.RequestHandler):
    def post(self):
        start = self.get_argument('from')
        end = self.get_argument('to')
        format = '%Y-%m-%d'
        start = datetime.datetime.strptime(start, format)
        end = datetime.datetime.strptime(end, format)
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        sql = 'select order_history.did,name,diet.price,sum(num) as number from order_history,diet where order_history.did = diet.did and stamp > %s and stamp < %s group by name' % (start, end)
        result = mysql.query(sql)
        response = {'status': 'ok', 'flow': result}
        self.write(json_encode(response))

class ManagerHistoryFeedbackHandler(tornado.web.RequestHandler):
    def post(self):
        start = self.get_argument('from')
        end = self.get_argument('to')
        format = '%Y-%m-%d'
        start = datetime.datetime.strptime(start, format)
        end = datetime.datetime.strptime(end, format)
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        sql = 'select diet.did,name,fb,sum(num) as number from order_history,feedback,diet where order_history.uid = feedback.uid and order_history.did = diet.did and order_history.stamp > %s and order_history.stamp < %s group by diet.did,fb' % (start, end)
        result = mysql.query(sql)
        temp = {}
        for one in result:
            did = one['did']
            fb = one['fb']
            temp[did]['did'] = did
            temp[did]['name'] = one['name']
            if fb == 1:
                temp[did]['good'] = one['number']
            elif fb == 0:
                temp[did]['normal'] = one['number']
            else:
                temp[did]['bad'] = one['number']
        feedback = temp.values()
        response = {'status': 'ok', 'fb': feedback}
        self.write(json_encode(response))

class ManagerHistoryTrendHandler(tornado.web.RequestHandler):
    def post(self):
        start = self.get_argument('from')
        end = self.get_argument('to')
        format = '%Y-%m-%d'
        start = datetime.datetime.strptime(start, format)
        end = datetime.datetime.strptime(end, format)
        if start >= end:
            return
        if start.day >28:
            return
        m = start
        t = []
        while m < end:
            year = m.year
            month = m.month
            day = m.day
            next_year = year
            next_month = month + 1
            if next_month > 12:
                next_year += 1
                next_month = 1
            next_day = day
            t.append((datetime.datetime(year,month,day), datetime.datetime(next_year,next_month,next_day)))
            m = datetime.datetime(next_year,next_month,next_day)
        s = []
        for one in t:
            start = one[0]
            end = one[1]
            start = time.mktime(start.timetuple())
            end = time.mktime(end.timetuple())
            s.append((start, end))
        
        trend = []
        for one in s:
            sql = 'select sum(order_history.price*num) as flow from order_history,diet where order_history.did = diet.did and stamp > %s and stamp < %s'
            sql = sql % one
            result = mysql.query(sql)
            flow = result[0]['flow']
            start = datetime.datetime.fromtimestamp(one[0])
            end = datetime.datetime.fromtimestamp(one[1])
            start = start.strftime(format)
            end = end.strftime(format)
            trend.append({'from': start, 'to': end, 'flow': flow})
        response = {'status': 'ok', 'trend': trend}
        self.write(json_encode(response))

class ManagerCommentHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-comment.html')

cursor = None
class ManagerCommentShowHandler(tornado.web.RequestHandler):
    def post(self):
        global cursor
        HOST = 'localhost'
        PORT = 3306
        USER = 'artoftime'
        PASSWD = 'artoftime'
        DB = 'artoftime'
        conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
        conn.autocommit(False)
        cursor = conn.cursor()
        sql = 'select * from comment'
        cursor.execute(sql)
        conn.commit()
        comments = cursor.fetchmany(100)
        response = {'status': 'ok', 'comments': comments}
        self.write(json_encode(response))

class ManagerCommentMoreHandler(tornado.web.RequestHandler):
    def post(self):
        global cursor
        comments = cursor.fetchmany(100)
        response = {'status': 'ok', 'comments': comments}
        self.write(json_encode(response))

class ManagerMaskHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-mask.html')

class ManagerMaskDietHandler(tornado.web.RequestHandler):
    def post(self):
        diet = mysql.get_all('diet')
        diet.sort(key=lambda one: one['cid'])
        response = {'status': 'ok', 'diet': diet}
        self.write(json_encode(response))

class ManagerMaskInsHandler(tornado.web.RequestHandler):
    def post(self):
        ins = json_decode(self.get_argument('ins'))
        logic.mask.ins(ins)
        response = {'status': 'ok'}
        self.write(json_encode(response))
        
class ManagerMaskUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        mymask = yield logic.mask.update(stamp)
        response = {'status': 'ok', 'mask': mymask, 'stamp': logic.mask.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()
        
        
        

    
        
