import tornado.web
import os
import logic
import mysql

from tornado.escape import json_encode, json_decode

class EntryHandler(tornado.web.RequestHandler):
    def get(self):
        heading = logic.info['heading']
        message = logic.info['welcome']
        self.render('entry.html', heading=heading, message=message)

    def post(self):
        desk = self.get_argument('desk')
        desk = desk.upper()
        if desk in logic.tables:
            response = {'status': 'ok'}
        else:
            response = {'status': 'error'}
        table = logic.tables.get(desk)
        if table is None:
            logic.tables[desk] = logic.Table(desk)
        self.write(json_encode(response))

class FacultyLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('fid')
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
        self.render('faculty-role.html', roles=roles, fid=fid)

    def post(self):
        role = self.get_argument('role')
        self.set_cookie('role', role)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class FacultySecretHandler(tornado.web.RequestHandler):
    def get(self):
        back = self.get_argument('back')
        self.render('faculty-secret.html', back=back)

    def post(self):
        fid = self.get_cookie('fid')
        passwd1 = self.get_argument('passwd1')
        passwd2 = self.get_argument('passwd2')
        result = mysql.get('password', {'fid': fid})
        #print result
        response = {'status': 'failure'}
        if result and result[0] and result[0]['passwd'] == passwd1:
            sql = 'update password set passwd = "%s" where fid = "%s"' % (passwd2, fid)
            #print sql
            r = mysql.execute(sql)
            #print r
            if r:
                response = {'status': 'success'}
        self.write(json_encode(response))
        

class PictureHandler(tornado.web.RequestHandler):
    def get(self, arg):
        #print "arg:", arg
        #self.set_header('Content-Type', 'application/octet-stream')
        #self.set_header('Content-Disposition', 'attachment; filename='+arg)
        path = os.path.join(logic.data_dir, 'pictures/'+arg)
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                while True:
                    data = f.read(40960)
                    if not data:
                        break
                    self.write(data)
        self.finish()
