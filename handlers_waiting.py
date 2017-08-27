import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class WaitingEntryHandler(tornado.web.RequestHandler):
    def get(self):
        cur = logic.ws.add()
        if cur == "sorry":
            self.write("Sorry, Queue is full! Please wait for a moment")
            return
        number = logic.ws.length() - 1
        self.set_cookie("waiting", str(cur))
        self.render("waiting-entry.html", message="welcome", th=cur, number=number)
        
    def post(self):
        cur = self.get_cookie('waiting')
        cur = int(cur)
        number = self.get_argument('number')
        #print type(number), number
        number = int(number)
        wtable = logic.WTable(cur, number)
        logic.waiting[cur] = wtable
        response = {'status': 'ok'}
        self.write(json_encode(response))

class WaitingCategoryHandler(tornado.web.RequestHandler):
    def get(self):
        waiting = self.get_cookie('waiting')
        self.render('waiting-category.html', table=waiting, category=logic.category)

class WaitingDietHandler(tornado.web.RequestHandler):
    def get(self):
        waiting = self.get_cookie('waiting')
        cid = self.get_argument('cid')
        group = []
        for k,v in logic.diet.items():
            if v['cid'] == cid:
                group.append(v)
        self.render('waiting-diet.html', table=waiting, diet=group, cid=cid)

class WaitingDetailHandler(tornado.web.RequestHandler):
    def get(self):
        did = self.get_argument('did')
        #print 'this is did:', type(did), did
        item = logic.diet.get(did)
        #print 'this is item:', item
        self.render('waiting-detail.html', item=item)
    
class WaitingInsHandler(tornado.web.RequestHandler):
    def post(self):
        waiting = self.get_cookie('waiting')
        ins = self.get_argument('ins')
        ins = json_decode(ins)
        #print 'ins:', ins
        r = logic.waiting_ins(waiting, ins)
        if r == 0:
            response = {'status': 'ok'}
        elif r is None:
            response = {'status': 'error'}
        self.write(json_encode(response))
        
class WaitingOrderHandler(tornado.web.RequestHandler):
    def get(self):
        waiting = self.get_cookie('waiting')
        self.render('waiting-order.html', table=waiting)

class WaitingUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        waiting = self.get_cookie('waiting')
        waiting = int(waiting)
        stamp = json_decode(self.get_argument('stamp'))
        wt = logic.waiting.get(waiting)
        myorder = yield wt.update(stamp)
        response = {'myorder': myorder}
        self.write(json_encode(response))
        raise tornado.gen.Return()
