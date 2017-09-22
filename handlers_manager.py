import tornado.web
import pickle
import logic
import mysql
import os

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
            
            if mysql.delete('diet', {'did': did}):
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
