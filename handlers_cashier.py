import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class CashierHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cashier-home.html')


class CashierWorkHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cashier-work.html')


class CashierWorkDeskHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        myorder = logic.tables.get(desk).to_dict()
        response = {'status': 'ok', 'myorder': myorder}
        self.write(json_encode(response))


class CashierWorkDeleteHandler(tornado.web.RequestHandler):
    def post(self):
        uid = self.get_argument('uid')
        uid = int(uid)
        one = logic.uids.get(uid)
        desk = one.desk
        one.cash_delete()
        myorder = logic.tables.get(desk).to_dict()
        response = {'status': 'ok', 'myorder': myorder}
        self.write(json_encode(response))

class CashierWorkCashHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        table = logic.tables.get(desk)
        fid = self.get_cookie('fid')
        result = table.cash(fid)
        response = {'status': result, 'myorder': table.to_dict()}
        self.write(json_encode(response))
        
        
