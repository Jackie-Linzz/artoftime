import tornado.web
import pickle
import datetime
import time
import logic
import logic_manager
import mysql
import os
import subprocess
import platform
#import qrcode
import MySQLdb
import printer
import prepare

from tornado.escape import json_encode, json_decode

class ManagerHomeHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-home.html')

class ManagerFacultyListHandler(tornado.web.RequestHandler):
    def post(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        faculty_list = mysql.get_all('faculty')
        faculty_list.sort(key=lambda x: x['fid'])
        #print faculty_list
        response = {'status': 'ok', 'faculty': faculty_list}
        self.write(json_encode(response))

class ManagerCompanyHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-company.html')

    def post(self):
        file = logic.company_file
        if not os.path.isfile(file):
            info =  {'company': '', 'shop': '', 'location': '', 'time': '', 'heading': '', 'welcome': '', 'desp': ''}
        else:
            with open(file, 'rb') as f:
                info = pickle.load(f)
        response = {'info': info}
        self.write(json_encode(response))

class ManagerCompanySetHandler(tornado.web.RequestHandler):
    def post(self):
        company = self.get_argument('company')
        shop = self.get_argument('shop')
        location = self.get_argument('location')
        work_time = self.get_argument('time')
        heading = self.get_argument('heading')
        welcome = self.get_argument('welcome')
        desp = self.get_argument('desp')
        #print work_time
        #content = company +'\n'+shop+'\n'+location+'\n'
        #print content
        #content = content.encode('gb18030')
        #printer.gprint(bytes(content))
        info = {'company': company, 'shop': shop, 'location': location, 'time': work_time, 'heading': heading, 'welcome': welcome, 'desp': desp}
        logic.info = info

        data_dir = logic.data_dir
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
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
        row = {'cid':cid, 'name': unicode(cname), 'ord': corder, 'desp': cdesp}
        result = mysql.insert('category', row)
        if result:
            logic.category[cid] = row
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerGroupDelHandler(tornado.web.RequestHandler):
    def post(self):
        cid = self.get_argument('cid')
        result = mysql.delete('category', {'cid': cid})
        if result:
            logic.category.pop(cid)
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
        who = self.get_argument('who', 'cook')
        #print who
        desp = self.get_argument('desp')
        
        order = int(order)
        price = float(price)
        price2 = float(price2)
        base = float(base)
        picture = ''
        pic_dir = os.path.join(logic.data_dir, 'pictures')
        if not os.path.isdir(pic_dir):
            os.mkdir(pic_dir)
        if self.request.files:
            metas = self.request.files['picture']
            for meta in metas:
                file_name = meta['filename']
                content = meta['body']
                ext = os.path.splitext(file_name)[-1]
                picture = str(did) + ext
                full_path = os.path.join(pic_dir, picture)
                with open(full_path, 'wb') as f:
                    f.write(content)
        row = {'did': did, 'name': name, 'ord': order, 'price': price, 'price2': price2, 'base': base, 'cid': cid, 'who': who, 'desp': desp, 'pic': picture}
        result = mysql.insert('diet', row)
        if result:
            logic.diet[did] = row
            response = {'status': 'ok'}
        else:
            if os.path.isfile(full_path):
                os.remove(full_path)
            response = {'status': 'error'}
        #content = name+'\n'+ ('%s' % price) +'\n'
        #content = content.encode('gb18030')
        #printer.gprint(bytes(content))
        self.write(json_encode(response))

class ManagerDietDelHandler(tornado.web.RequestHandler):
    def post(self):
        did = self.get_argument('did')
        if did in logic.diet:
            logic.diet.pop(did)
        result = mysql.get('diet', {'did': did})
        if result and result[0]:
            picture = result[0]['pic']
            full_path = os.path.join(logic.data_dir, 'pictures/' + picture)
            
            if mysql.delete('diet', {'did': did}) and picture != '':
                if os.path.isfile(full_path):
                    os.remove(full_path)

            response = {'status': 'ok'}
            self.finish(json_encode(response))
            return
        response = {'status': 'error'}
        self.finish(json_encode(response))

class ManagerDietShowHandler(tornado.web.RequestHandler):
    def post(self):
        result = mysql.get_all('diet');
        result.sort(key=lambda one: one['did'])
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
        seats = self.get_argument('seats')
        seats = int(seats)
        result = mysql.insert('desks', {'desk': desk, 'num': seats})
        
        if result:
            #path = os.path.join(logic.data_dir, 'desks/' + desk)
            #data = desk
            #img = qrcode.make(data)
            #img.save(path)
            if desk not in logic.desks:
                logic.desks.add(desk)
            if desk not in logic.tables:
                logic.tables[desk] = logic.Table(desk)
            response = {'status': 'ok'}
        else:
            
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerDeskDelHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        result = mysql.delete('desks', {'desk': desk})
        if desk in logic.desks:
            logic.desks.remove(desk)
        if desk in logic.tables:
            logic.tables.pop(desk)
        if result:
            #path = os.path.join(logic.data_dir, 'desks/' + desk)
            #os.remove(path)
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class ManagerDeskShowHandler(tornado.web.RequestHandler):
    def post(self):
        desks = mysql.get_all('desks')
        desks.sort(key=lambda x: x['desk'])
        response = {'status': 'ok', 'desks': desks}
        self.write(json_encode(response))

class ManagerOrderHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-order.html')

    def post(self):
        pid = self.get_argument('order')
        pid = int(pid)
        sql = 'select order_history.uid as uid,diet.name as name,num,order_history.price as price,cook_history.fid as cook,cash_history.fid as cashier,status from cash_history,order_history,cook_history,diet where cash_history.uid=order_history.uid and order_history.uid=cook_history.uid and order_history.did=diet.did and order_history.pid=%s' % pid
        result = mysql.query(sql)
        print result
        result2 = mysql.get_all('faculty')
        faculty = {}
        for one in result2:
            faculty[one['fid']] = one['name']
        total = 0
        for one in result:
            one['price'] = one['num'] * one['price']
            one['cook'] = faculty[one['cook']]
            one['cashier'] = faculty[one['cashier']]
            if one['status'] == 'success':
                total += one['price']
        result.append({'name': '', 'num': 'all', 'price': total, 'cook': '', 'cashier': '', 'status': ''})
        response = {'status': 'ok', 'pid': pid, 'items': result}
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
        result.sort(key=lambda x: x['fid'])
        #print result
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
        #print fid
        
        results = []
        if fid == 'all':
            faculty = mysql.get_all('faculty')
            for one in faculty:
                if one['role'].find('cook') >=0:
                    results.append({'fid': one['fid'], 'name': one['name'], 'diet': logic_manager.get_cook_range(one['fid'])})
        else:
            name = logic.faculty.get(fid)['name']
            results.append({'fid': fid, 'name': name, 'diet': logic_manager.get_cook_range(fid)})
        response = {'status': 'ok', 'result': results}
        
        self.write(json_encode(response))

class ManagerTodayHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-today.html')
    def post(self):
        now = datetime.datetime.now()
        start = datetime.datetime(now.year, now.month, now.day)
        end = start + datetime.timedelta(days=1)
        t1 = start.strftime('%Y-%m-%d')
        t2 = end.strftime('%Y-%m-%d')
        rows = logic_manager.flow_data(start, end)
        flow = [{'type': '', 'from': t1, 'to': t2, 'rows': rows}]
        frequency = logic_manager.frequency(now, request=1, kitchen=1, cash=1)
        cooks = []
        for fid in logic.working_cooks:
            rows = logic_manager.one_cook_flow(fid, start, end)
            #print 'one_cook_flow:', rows
            name = logic.faculty.get(fid)['name']
            cooks.append({'fid': fid, 'name': name, 'rows': rows, 'type': 'cook'})
        response = {'status': 'ok', 'flow': flow, 'frequency': frequency, 'cooks': cooks}
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
        trend = self.get_argument('trend')
        trend = int(trend)
        #print t1, t2
        format = '%Y-%m-%d'
        t1 = datetime.datetime.strptime(t1, format)
        t2 = datetime.datetime.strptime(t2, format)
        #print t1, t2
        if t1 >= t2:
            return
        result = logic_manager.achieve(fid, t1, t2, trend)
        #print result
        response = {'status': 'ok', 'result': result}
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
        trend = self.get_argument('trend')
        trend = int(trend)
        format = '%Y-%m-%d'
        start = datetime.datetime.strptime(start, format)
        end = datetime.datetime.strptime(end, format)
        result = logic_manager.flow(start, end, trend)
        #print result
        response = {'status': 'ok', 'result': result}
        self.write(json_encode(response))
        

class ManagerHistoryFeedbackHandler(tornado.web.RequestHandler):
    def post(self):
        pass

class ManagerHistoryTrendHandler(tornado.web.RequestHandler):
    def post(self):
        pass

class ManagerOnedietHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-onediet.html')

    def post(self):
        did = self.get_argument('did')
        start = self.get_argument('from')
        end = self.get_argument('to')
        trend = self.get_argument('trend')
        trend = int(trend)
        format = '%Y-%m-%d'
        start = datetime.datetime.strptime(start, format)
        end = datetime.datetime.strptime(end, format)
        result = logic_manager.one_diet(did, start, end, trend)
        response = {'status': 'ok', 'result': result}
        self.write(json_encode(response))

class ManagerFrequencyHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-frequency.html')

    def post(self):
        day = self.get_argument('date')
        request = self.get_argument('request')
        kitchen = self.get_argument('kitchen')
        cash = self.get_argument('cash')
        request = int(request)
        kitchen = int(kitchen)
        cash = int(cash)
        format = '%Y-%m-%d'
        day = datetime.datetime.strptime(day, format)
        result = logic_manager.frequency(day,request=request, kitchen=kitchen, cash=cash)
        response = {'status': 'ok', 'result': result}
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
        sql = 'select * from comment order by stamp desc'
        cursor.execute(sql)
        conn.commit()
        comments = cursor.fetchmany(100)
        #print comments
        result = []
        for one in comments:
            stamp = one[3]
            stamp = datetime.datetime.fromtimestamp(stamp)
            stamp = stamp.strftime('%Y-%m-%d %H:%M:%S')
            t = {'desk': one[1], 'comment': one[2], 'stamp': stamp}
            result.append(t)
        response = {'status': 'ok', 'comments': result}
        self.write(json_encode(response))

class ManagerCommentMoreHandler(tornado.web.RequestHandler):
    def post(self):
        global cursor
        comments = cursor.fetchmany(100)
        result = []
        for one in comments:
            stamp = one[3]
            stamp = datetime.datetime.fromtimestamp(stamp)
            stamp = stamp.strftime('%Y-%m-%d %H:%M:%S')
            t = {'desk': one[1], 'comment': one[2], 'stamp': stamp}
            result.append(t)
        response = {'status': 'ok', 'comments': result}
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
        diet.sort(key=lambda one: one['did'])
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


class ManagerShutdownHandler(tornado.web.RequestHandler):
    def get(self):
        role = self.get_cookie('role')
        if role != 'manager':
            return
        self.render('manager-shutdown.html')

    def post(self):
        #prepare.save()
        if platform.system() == 'Darwin':
            echo = subprocess.Popen(['echo', 'jerrylan418'], stdout=subprocess.PIPE)
            shutdown = subprocess.Popen(['sudo', '-S', 'shutdown', '-h', 'now'], stdin=echo.stdout)
        elif platform.system() == 'Linux':
            echo = subprocess.Popen(['echo', 'lin890418\n'], stdout=subprocess.PIPE)
            shutdown = subprocess.Popen(['sudo', '-S', 'shutdown', '-P', 'now'], stdin=echo.stdout)
        
class ManagerRebootHandler(tornado.web.RequestHandler):
    def post(self):
        #prepare.save()
        if platform.system() == 'Darwin':
            echo = subprocess.Popen(['echo', 'jerrylan418'], stdout=subprocess.PIPE)
            reboot = subprocess.Popen(['sudo', '-S', 'reboot'], stdin=echo.stdout)
        elif platform.system() == 'Linux':
            echo = subprocess.Popen(['echo', 'lin890418\n'], stdout=subprocess.PIPE)
            reboot = subprocess.Popen(['sudo', '-S', 'reboot'], stdin=echo.stdout)
        
        

    
        
