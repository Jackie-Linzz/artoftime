import tornado.web
import logic

class WaiterHomeHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_cookie('fid')
        self.render('waiter-home.html', fid=fid)
