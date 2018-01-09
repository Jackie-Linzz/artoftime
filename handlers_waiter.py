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

class WaiterOrderUpdateHandler(tornado.web.RequestHandler):
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

class WaiterPassHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-pass.html', fid=fid)

class WaiterPassRemoveHandler(tornado.web.RequestHandler):
    def post(self):
        uid = self.get_argument('uid')
        uid = int(uid)
        logic.passmsg.remove(uid)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class WaiterPassUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        message = yield logic.passmsg.update(stamp)
        response = {'status': 'ok', 'message': message, 'stamp': logic.passmsg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()


class WaiterFeedbackHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-feedback.html', fid=fid)

class WaiterFeedbackRemoveHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk').upper()
        logic.feedbackmsg.remove(desk)
        response = {'status': 'ok'}
        self.write(json_encode(response))


class WaiterFeedbackUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        message = yield logic.feedbackmsg.update(stamp)
        response = {'status': 'ok', 'message': message, 'stamp': logic.feedbackmsg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()


class WaiterRequestHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-request.html', fid=fid)

class WaiterRequestRemoveHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk').upper()
        logic.requestmsg.remove(desk)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class WaiterRequestUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        message = yield logic.requestmsg.update(stamp)
        response = {'status': 'ok', 'message': message, 'stamp': logic.requestmsg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()

class WaiterMaskHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-mask.html', fid=fid)

class WaiterCleanHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-clean.html', fid=fid)

class WaiterCleanRemoveHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk').upper()
        logic.cleanmsg.remove(desk)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class WaiterCleanUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        message = yield logic.cleanmsg.update(stamp)
        response = {'status': 'ok', 'message': message, 'stamp': logic.cleanmsg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()

    
