import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.iostream
import os


from tornado.options import define, options

from handlers_waiting import *
from handlers_common import *
from handlers_customer import *

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")



myhandlers = [(r'/waiting-entry', WaitingEntryHandler),
              (r'/waiting-category', WaitingCategoryHandler),
              (r'/waiting-diet', WaitingDietHandler),
              (r'/waiting-detail', WaitingDetailHandler),
              (r'/waiting-ins', WaitingInsHandler),
              (r'/waiting-order', WaitingOrderHandler),
              (r'/waiting-update', WaitingUpdateHandler),
              (r'/entry', EntryHandler),
              (r'/customer-home', CustomerHomeHandler),
              (r'/customer-category', CustomerCategoryHandler),
              (r'/customer-diet', CustomerDietHandler),
              (r'/customer-detail', CustomerDetailHandler),
              (r'/customer-order', CustomerOrderHandler),
              (r'/customer-ins', CustomerInsHandler),
              (r'/customer-update', CustomerUpdateHandler),
              (r'/customer-feedback', CustomerFeedbackHandler)]
settings = dict(
                cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
               # login_url="/",
                template_path=os.path.join(os.getcwd(), "templates"),
                static_path=os.path.join(os.getcwd(), "static"),
                xsrf_cookies=False,
                debug=options.debug,
                )


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application(myhandlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




if __name__ == "__main__":
    main()


