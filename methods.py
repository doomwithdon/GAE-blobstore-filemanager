# -*- coding:UTF-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from models import *

import logging

#user api
def user_system(current_user):
    if current_user:
        loginout_url = users.create_logout_url('/')
    else:
        loginout_url = users.create_login_url('/')

#載入Bandwidth_log
def load_Bandwidth_log():
    log_key = db.Key.from_path("Bandwidth_log","Quota")
    log_info = db.get(log_key)
    #如果沒有table，則立刻建立一個新的table
    if log_info is None:
        log_put = Bandwidth_log(key_name="Quota",
                             Upload_Bandwidth = 1024**3,
                             Download_Bandwidth =1024**3)
        log_put.put()
        log_info = log_put
    return log_info