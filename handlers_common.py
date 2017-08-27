import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class EntryHandler(tornado.web.RequestHandler):
    def get(self):
        heading = 'ART OF TIME'
        message = 'welcome'
        self.render('entry.html', heading=heading, message=message)

    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        if desk in logic.desks:
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        table = logic.tables.get(desk)
        if table is None:
            logic.tables[desk] = logic.Table(desk)
        self.write(json_encode(response))
