import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class WaiterHomeHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        if logic.waiters.get(fid) == None:
            logic.waiters[fid] = logic.Waiter(fid)
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
        fid = self.get_cookie('fid');
        waiter = logic.waiters.get(fid)
        uid = self.get_argument('uid')
        uid = int(uid)
        logic.passmsg.remove(uid)
        waiter.passl(uid)
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

class WaiterStatusUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        message = yield logic.statusmsg.update(stamp)
        response = {'status': 'ok', 'message': message, 'stamp': logic.statusmsg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()

class WaiterReceiveHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('waiter-receive.html')

        
class WaiterDoneHandler(tornado.web.RequestHandler):
    def post(self):
        fid = self.get_cookie('fid')
        uid = self.get_argument('uid', None)
        print type(uid)
        uid = int(uid)
        if uid is None:
            return
        waiter = logic.waiters.get(fid)
        waiter.receive(uid)

class WaiterLeftUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        left = yield logic.left2msg.update(stamp)
        response = {'status': 'ok', 'left': left, 'stamp': logic.left2msg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()

class WaiterDoneUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        fid = self.get_cookie('fid')
        waiter = logic.waiters.get(fid)
        stamp = json_decode(self.get_argument('stamp'))
        done = yield waiter.update(stamp)
        response = {'status': 'ok', 'done': done, 'stamp': waiter.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()


class WaiterQueryHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        diet = logic.diet.values()
        diet.sort(key=lambda x: x['did'])
        self.render('waiter-query.html', fid=fid, diet=diet)

class WaiterQueueHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-queue.html', fid=fid)

    def post(self):
        order = self.get_argument('order')
        order = int(order)
        logic.queue.remove(order)
        self.write('ok')

class WaiterDeskUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        
        stamp = json_decode(self.get_argument('stamp'))
        desks = yield logic.idle_desks.update(stamp)
        response = {'status': 'ok', 'desks': desks, 'stamp': logic.idle_desks.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()

class WaiterQueueUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        queue = yield logic.queue.update(stamp)
        response = {'status': 'ok', 'queue': queue, 'stamp': logic.queue.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()
