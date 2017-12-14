import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class WaiterHomeHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-home.html', fid=fid)


class WaiterOrderHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('waiter-order.html')


class WaiterInsHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        ins = json_decode(self.get_argument('ins'))
        logic.waiter_ins(desk, ins)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class WaiterUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        stamp = json_decode(self.get_argument('stamp'))
        table = logic.tables.get(desk)
        myorder = yield table.update(stamp)
        response = {'myorder': myorder}
        self.write(json_encode(response))
        raise tornado.gen.Return()
