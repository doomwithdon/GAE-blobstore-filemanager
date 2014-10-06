# -*- coding:UTF-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from models import *

import logging
import datetime

#載入log
def load_log(entity,key_name):
    #因為我以"時間"型態命名Upload_log和Download_log的key_name
    #為了讓時間型態轉換成字串型態，必須加以小心註記
    log_key = db.Key.from_path(entity,str(key_name))
    log_info = db.get(log_key)
    if log_info is None:
        if entity == "Bandwidth_log" :
            #使用為("Bandwidth_log","Quota")
            log_put = Bandwidth_log(key_name=key_name,
                                    Upload_Bandwidth = 1024**3,
                                    Download_Bandwidth =1024**3)
        elif entity == "Upload_log" :
            #使用為("Upload_log",某時間)
            log_put = Upload_log(key_name=str(key_name),
                                 Usage_Bandwidth = 0,
                                 date=key_name)
        elif entity == "Download_log" :
            #使用為("Download_log",某時間)
            log_put = Download_log(key_name=str(key_name),
                                   Usage_Bandwidth = 0,
                                   date=key_name)
        log_put.put()
        log_info = log_put
    return log_info

class Stored_Data_Details:
    def __init__(self):
        #硬碟使用總量
        self.wrapper_total_size = 0
        for wrapper in Wrapper.all():
            self.wrapper_total_size += wrapper.blob.size
        #你的硬碟使用量
        self.your_usage = 0        
        your_files = Wrapper.all()
        your_files.filter("user =", users.get_current_user())
        for your_file in your_files :
            self.your_usage += your_file.blob.size
        #其他人的硬碟使用量
        self.else_users_usage = self.wrapper_total_size - self.your_usage
        #剩餘空間
        self.no_usage = 5 * 1024**3 - self.wrapper_total_size
    def Your_usage(self):
        return self.your_usage 
    def Else_users_usage(self):
        return self.else_users_usage 
    def No_usage(self):
        return self.no_usage
    def Total_usage(self):
        return self.wrapper_total_size