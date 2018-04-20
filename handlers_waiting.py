import tornado.web
import logic

from tornado.escape import json_encode, json_decode

class WaitingEntryHandler(tornado.web.RequestHandler):
    def get(self):
        message = logic.info['welcome']
        self.render('waiting-entry.html', message=message)
        
    def post(self):
        
        number = self.get_argument('number')
        #print type(number), number
        number = int(number)
        order = logic.queue_cursor
        self.set_cookie('order', str(order))
        logic.queue.add(number)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class WaitingQueueHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('waiting-queue.html')

