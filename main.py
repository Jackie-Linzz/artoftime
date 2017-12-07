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
from handlers_manager import *
from handlers_cook import *
from handlers_cashier import *

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
              (r'/customer-feedback', CustomerFeedbackHandler),
              (r'/faculty-login', FacultyLoginHandler),
              (r'/faculty-role', FacultyRoleHandler),
              (r'/faculty-secret', FacultySecretHandler),
              (r'/manager-home', ManagerHomeHandler),
              (r'/manager-company', ManagerCompanyHandler),
              (r'/manager-company-set', ManagerCompanySetHandler),
              (r'/manager-diet', ManagerDietHandler),
              (r'/manager-group-add', ManagerGroupAddHandler),
              (r'/manager-group-del', ManagerGroupDelHandler),
              (r'/manager-group-show', ManagerGroupShowHandler),
              (r'/manager-diet-add', ManagerDietAddHandler),
              (r'/manager-diet-del', ManagerDietDelHandler),
              (r'/manager-diet-show', ManagerDietShowHandler),
              (r'/manager-desk', ManagerDeskHandler),
              (r'/manager-desk-add', ManagerDeskAddHandler),
              (r'/manager-desk-del', ManagerDeskDelHandler),
              (r'/manager-desk-show', ManagerDeskShowHandler),
              (r'/manager-worker', ManagerWorkerHandler),
              (r'/manager-worker-add', ManagerWorkerAddHandler),
              (r'/manager-worker-del', ManagerWorkerDelHandler),
              (r'/manager-worker-show', ManagerWorkerShowHandler),
              (r'/manager-cookdo', ManagerCookdoHandler),
              (r'/manager-achievement', ManagerAchievementHandler),
              (r'/manager-history', ManagerHistoryHandler),
              (r'/manager-history-flow', ManagerHistoryFlowHandler),
              (r'/manager-history-fb', ManagerHistoryFeedbackHandler),
              (r'/manager-history-trend', ManagerHistoryTrendHandler),
              (r'/manager-comment', ManagerCommentHandler),
              (r'/manager-comment-show', ManagerCommentShowHandler),
              (r'/manager-comment-more', ManagerCommentMoreHandler),
              (r'/manager-mask', ManagerMaskHandler),
              (r'/manager-mask-diet', ManagerMaskDietHandler),
              (r'/manager-mask-ins', ManagerMaskInsHandler),
              (r'/manager-mask-update', ManagerMaskUpdateHandler),
              (r'/cook-home', CookHomeHandler),
              (r'/cook-do', CookDoHandler),
              (r'/cook-do-submit', CookDoSubmitHandler),
              (r'/cook-work', CookWorkHandler),
              (r'/cook-ins', CookInsHandler),
              (r'/cook-work-update', CookWorkUpdateHandler),
              (r'/cashier-home', CashierHomeHandler),
              (r'/cashier-work', CashierWorkHandler),
              (r'/cashier-work-desk', CashierWorkDeskHandler),
              (r'/cashier-work-delete', CashierWorkDeleteHandler),
              (r'/cashier-work-cash', CashierWorkCashHandler)]
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


