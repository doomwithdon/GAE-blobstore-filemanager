# -*- coding:UTF-8 -*-
#!/usr/bin/env python

#python內建函式庫
import os
import logging

#GAE的函式庫
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore, db, webapp
from google.appengine.ext.webapp import blobstore_handlers, template

#自創函式庫
import methods
from models import *
from backend_process import *
#--------------------------------------------------------------------
#對前端框架的模板語法註冊新功能
webapp.template.register_template_library('filterdir.customfilters')
#--------------------------------------------------------------------
#('/', Home_Handler)
class Home_Handler(webapp2.RequestHandler):
    def get(self):
        methods.user_system(users.get_current_user()) 

        values = {
            'user': users.get_current_user(),
            'users': users,
            'startup_web':"home",
        }        
        path = os.path.join(os.path.dirname(__file__), 'html','home.html')
        self.response.out.write(template.render(path, values))


#('/clouddrive', Clouddrive_Handler)
class Clouddrive_Handler(webapp2.RequestHandler):
    def get(self):

        owner_usage = 0
        if users.get_current_user():
            loginout_url = users.create_logout_url('/')
            #取得用戶使用硬碟份量
            owner_file = Wrapper.all()
            owner_file.filter("user =", users.get_current_user())
            for wrapper in owner_file:
                owner_usage += wrapper.blob.size    
        else:
            loginout_url = users.create_login_url('/')

        logging.info("================================")

        
        wrapper_total_size = 0
        for wrapper in Wrapper.all():
            wrapper_total_size += wrapper.blob.size
        

        #列出用戶名單
        owner_list = db.GqlQuery("SELECT DISTINCT user FROM Wrapper")

        logging.info("================================")

        Bandwidth_log_Quota = methods.load_Bandwidth_log()


        values = {
            'user': users.get_current_user(),
            'users': users,
            'upload_url': blobstore.create_upload_url('/upload'),
            'wrappers': Wrapper.all().order('-date'),
            'wrapper_total_size':wrapper_total_size,
            'owner_usage':owner_usage,
            'owner_list':owner_list,
            'startup_web':"clouddrive",
            'Bandwidth_log':Bandwidth_log_Quota,
        }
            
        path = os.path.join(os.path.dirname(__file__), 'html','clouddrive.html')
        self.response.out.write(template.render(path, values))

#('/charts', Charts_Handler)
class Charts_Handler(webapp2.RequestHandler):
    def get(self):  
        values = {
        }  
        path = os.path.join(os.path.dirname(__file__), 'html','charts.html')
        self.response.out.write(template.render(path, values))

class Test_Handler(webapp2.RequestHandler):
    def get(self):
        values = {
        }        
        
        path = os.path.join(os.path.dirname(__file__), 'html','yuntrun.htm')
        self.response.out.write(template.render(path, values))

#網址啟動
app = webapp2.WSGIApplication([
    #前端輸出
    ('/', Home_Handler),
    ('/clouddrive', Clouddrive_Handler),
    ('/charts', Charts_Handler),
    ('/account', Account_Handler),
    ('/test1', Test_Handler),

    #後端處理
    ('/upload', Upload_Handler),
    ('/serve/([^/]+)?', Serve_Handler),
    ('/delete', Delete_Handler),
], debug=True)
