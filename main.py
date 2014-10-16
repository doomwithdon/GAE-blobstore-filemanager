# -*- coding:UTF-8 -*-
#!/usr/bin/env python

#python內建函式庫
import os
import logging
import datetime
import time
import csv

#GAE的函式庫
import webapp2
from google.appengine.api import users
from google.appengine.ext import blobstore, db, webapp
from google.appengine.ext.webapp import blobstore_handlers, template

#自創函式庫
import methods
from models import *
from backend_process import *
from instant_messaging import *
from cron import *
from filterdir.customfilters import *

#--------------------------------------------------------------------
#對前端框架的模板語法註冊新功能
webapp.template.register_template_library('filterdir.customfilters')
#--------------------------------------------------------------------
#('/', Home_Handler)
class Home_Handler(webapp2.RequestHandler):
    def get(self):
        values = {
            'startup_web':"home",
        }        
        path = os.path.join(os.path.dirname(__file__), 'html','home.html')
        self.response.out.write(template.render(path, values))


#('/clouddrive', Clouddrive_Handler)
class Clouddrive_Handler(webapp2.RequestHandler):
    def get(self):
        #獲取使用者對於資料庫空間使用情形
        stored_data_details = methods.Stored_Data_Details()
        #獲取目前頻寬狀態
        Bandwidth_log_Quota = methods.load_log("Bandwidth_log","Quota")
        values = {
            'user': users.get_current_user(),
            'users': users,
            'stored_data_details':stored_data_details,
            'upload_url': blobstore.create_upload_url('/upload'),
            'wrappers': Wrapper.all().order('-date'),
            'startup_web':"clouddrive",
            'Bandwidth_log':Bandwidth_log_Quota,
        }
            
        path = os.path.join(os.path.dirname(__file__), 'html','clouddrive.html')
        self.response.out.write(template.render(path, values))

#('/dashboard', Charts_Handler)
class Dashboard_Handler(webapp2.RequestHandler):
    def get(self):
        #獲取使用者對於資料庫空間使用情形
        stored_data_details = methods.Stored_Data_Details()
        #獲取log
        Bandwidth_log_Quota = methods.load_log("Bandwidth_log","Quota")
        Upload_log_Quota = Upload_log.all().order('date')#由舊到新
        Download_log_Quota = Download_log.all().order('date')#由舊到新

        logging.info("====================================")
        logging.info(datetime.datetime.now().date())
        t = time.time()
        # 透過 datetime
        logging.info(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'))
        values = {
            'user': users.get_current_user(),
            'users': users,
            'stored_data_details':stored_data_details,
            'startup_web':"dashboard",
            'Bandwidth_log':Bandwidth_log_Quota,
            'Upload_log':Upload_log_Quota,
            'Download_log':Download_log_Quota,
        }  
        path = os.path.join(os.path.dirname(__file__), 'html','dashboard.html')
        self.response.out.write(template.render(path, values))

#('/instant_messaging', Instant_Messaging_Handler)
class Instant_Messaging_Handler(webapp2.RequestHandler):
    def get(self):
        values = {
            'startup_web':"instant_messaging",
        }        
        path = os.path.join(os.path.dirname(__file__), 'html','instant_messaging.html')
        self.response.out.write(template.render(path, values))

class Test_Handler(webapp2.RequestHandler):
    def get(self):
        pass

#網址啟動
app = webapp2.WSGIApplication([
    #前端輸出
    ('/', Home_Handler),
    ('/clouddrive', Clouddrive_Handler),
    ('/dashboard', Dashboard_Handler),
    ('/account/([^/]+)?', Account_Handler),
    ('/test1', Test_Handler),
    ('/instant_messaging', Instant_Messaging_Handler),
    #後端處理
    ('/upload', Upload_Handler),
    ('/serve/([^/]+)?', Serve_Handler),
    ('/delete', Delete_Handler),
    ('/csv', CSV_Handler),
    #即時通功能
    ('/post_msg', ReceiveHandler),
    ('/get_token', GetTokenHandler),
    ('/del_token', ReleaseTokenHandler),
    ('/open', OpenHandler),
    #排程
    ('/quotas_reset', Quotas_Reset_Handler),
], debug=True)
