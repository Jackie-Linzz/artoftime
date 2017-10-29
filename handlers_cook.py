import tornado.web
import logic
import mysql

from tornado.escape import json_encode, json_decode

class CookHomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cook-home.html')
        
class CookDoHandler(tornado.web.RequestHandler):
    def get(self):
        diet = mysql.get_all('diet')
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
