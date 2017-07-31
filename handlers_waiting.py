import tornado.web

class WaitingEntryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("waiting-entry.html")
        
