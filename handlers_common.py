import tornado.web
import logic
import mysql

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

class FacultyLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('faculty-login.html')

    def post(self):
        #import pdb
        #pdb.set_trace()
        fid = self.get_argument('fid')
        passwd = self.get_argument('passwd')
        result = mysql.get('password', {'fid': fid})
        response = {'status': 'error'}
        if len(result) == 1:
            if passwd == result[0]['passwd']:
                self.set_cookie('fid', fid)
                response = {'status': 'ok'}
        self.write(json_encode(response))
        
class FacultyRoleHandler(tornado.web.RequestHandler):
    def get(self):
        #import pdb
        #pdb.set_trace()
        fid = self.get_cookie('fid')
        self.clear_cookie('role')
        roles = mysql.get('faculty', {'fid': fid})
        if len(roles) == 0:
            return
        roles = roles[0]['role']
        roles = roles.split(',')
        self.render('faculty-role.html', roles=roles)

    def post(self):
        role = self.get_argument('role')
        self.set_cookie('role', role)
        response = {'status': 'ok'}
        self.write(json_encode(response))
