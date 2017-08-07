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
        number = self.get_argument('number')
        #print type(number), number
        number = int(number)
        response = {'status': 'ok'}
        self.write(json_encode(response))
