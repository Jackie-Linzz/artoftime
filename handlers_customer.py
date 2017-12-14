import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class CustomerHomeHandler(tornado.web.RequestHandler):
    def get(self):
        desk = self.get_argument('desk')
        self.render('customer-home.html', table=desk)

class CustomerCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        groups = logic.category.values()
        groups = sorted(groups, key=lambda x: x['ord'])
        self.render('customer-category.html', table=desk, groups=groups)

class CustomerDietHandler(tornado.web.RequestHandler):
    def get(self):
        desk = self.get_argument('desk').upper()
        cid = self.get_argument('cid')
        group = []
        for k, v in logic.diet.items():
            if v['cid'] == cid:
                group.append(v)
        cname = logic.category.get(cid)['name']
        self.render('customer-diet.html', table=desk, cname=cname, group=group, cid=cid)
        
class CustomerDetailHandler(tornado.web.RequestHandler):
    def get(self):
        desk = self.get_argument('desk')
        did = self.get_argument('did')
        item = logic.diet.get(did)
        self.render('customer-detail.html', table=desk, did=did, item=item)

class CustomerOrderHandler(tornado.web.RequestHandler):
    def get(self):
        desk = self.get_argument('desk')
        self.render('customer-order.html', table=desk)

class CustomerInsHandler(tornado.web.RequestHandler):
    def post(self):
        desk = self.get_argument('desk')
        ins = json_decode(self.get_argument('ins'))
        logic.customer_ins(desk, ins)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class CustomerUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        desk = self.get_argument('desk').upper()
        stamp = json_decode(self.get_argument('stamp'))
        table = logic.tables.get(desk)
        myorder = yield table.update(stamp)
        response = {'myorder': myorder}
        self.write(json_encode(response))
        raise tornado.gen.Return()

class CustomerFeedbackHandler(tornado.web.RequestHandler):
    def get(self):
        desk = self.get_argument('desk')
        table = logic.tables.get(desk)
        self.render('customer-feedback.html', table=desk, done=table.done)

    def post(self):
        desk = self.get_argument('desk')
        comment = json_decode(self.get_argument('comment'))
        fb = json_decode(self.get_argument('fb'))
        table = logic.tables.get(desk)
        table.comment = comment
        table.feedback(fb)
        response = {'status': 'ok'}
        self.write(json_encode(response))
        
