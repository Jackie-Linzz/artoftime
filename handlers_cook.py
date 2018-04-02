import tornado.web
import logic
import mysql

from tornado.escape import json_encode, json_decode

class CookHomeHandler(tornado.web.RequestHandler):
    def get(self):
        #install cook in cooks
        fid = self.get_cookie('fid')
        logic.working_cooks.add(fid)
        if logic.cooks.get(fid) == None:
            logic.cooks[fid] = logic.Cook(fid)
        self.render('cook-home.html')
        
class CookDoHandler(tornado.web.RequestHandler):
    def get(self):
        diet = []
        for k, v in logic.diet.items():
            if v['who'] == 'cook':
                diet.append(v)
        diet = sorted(diet, key=lambda one: one['did'])
        self.render('cook-do.html',diet=diet)

    def post(self):
        fid = self.get_cookie('fid')
        cookdo = []
        result = mysql.get('cook_do', {'fid': fid})
        flag = False
        for one in result:
            if one['did'] == 'all':
                flag = True
                break
            cookdo.append(one['did'])
        if flag == True:
            cookdo = ['all']
        response = {'status': 'ok', 'cookdo': cookdo}
        self.write(json_encode(response))

class CookDoSubmitHandler(tornado.web.RequestHandler):
    def post(self):
        fid = self.get_cookie('fid')
        content = json_decode(self.get_argument('content'))
        mysql.delete('cook_do', {'fid': fid})
        flag = False
        for did in content:
            if did == 'all':
                flag = True
                break
        if flag:
            rows = [{'fid': fid, 'did': 'all'}]
        else:
            rows = []
            for did in content:
                rows.append({'fid':fid, 'did': did})
        result = mysql.insert_many('cook_do', rows)
        if result:
            logic.cooks.get(fid).cookdo = content
            response = {'status': 'ok', 'cookdo': content}
        else:
            response = {'status': 'error'}
        self.write(json_encode(response))

class CookWorkHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cook-work.html')

class CookInsHandler(tornado.web.RequestHandler):
    def post(self):
        fid = self.get_argument('fid')
        ins = json_decode(self.get_argument('ins'))
        cook = logic.cooks.get(fid)
        cook.ins(ins)
        response = {'status': 'ok'}
        self.write(json_encode(response))

class CookWorkUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        fid = self.get_argument('fid')
        stamp = json_decode(self.get_argument('stamp'))
        cook = logic.cooks.get(fid)
        thecook = yield cook.update(stamp)
        response = {'cook': thecook}
        self.write(json_encode(response))
        raise tornado.gen.Return()

class CookLeftUpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        stamp = json_decode(self.get_argument('stamp'))
        left = yield logic.leftmsg.update(stamp)
        response = {'left': left, 'stamp': logic.leftmsg.stamp}
        self.write(json_encode(response))
        raise tornado.gen.Return()
        
    
