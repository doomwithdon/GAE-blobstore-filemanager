# -*- coding:UTF-8 -*-
import webapp2

from models import *
import logging

import urllib
import datetime
import time
import methods
import csv
from filterdir.customfilters import *

from google.appengine.api import users
from google.appengine.ext import db,blobstore, webapp
from google.appengine.ext.webapp import blobstore_handlers

#上傳檔案
#('/upload', Upload_Handler)
class Upload_Handler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            #接收前端form的檔案
            upload_files = self.get_uploads('file')        
            total_size = 0 
            if len(upload_files) > 0:   
                logging.info(upload_files)
                for blob_info in upload_files :
                    #進行Wrapper寫入作業
                    blob_key = blob_info.key() #註冊key
                    blob_filename = str(blob_info.filename) #取得filename 
                    blob_content_type = str(blob_info.content_type) #取得檔案類型
                    #logging.info(blob_content_type) #測試
                    Wrapper(blob=blob_key,
                            filename=blob_filename,
                            content_type=blob_content_type).put()
                    #計算檔案總大小
                    total_size += blob_info.size
            #計算完畢後，進行Upload_log寫入作業
            now = datetime.datetime.now().date()
            log_info = methods.load_log("Upload_log",now)
            log_info.Usage_Bandwidth += total_size
            log_info.put()
            #Bandwidth_log更新作業
            log_info = methods.load_log("Bandwidth_log","Quota")
            log_info.Upload_Bandwidth -= total_size
            log_info.put()
            self.redirect('/clouddrive')
        except CapabilityDisabledError:
            self.response.out.write('Uploading disabled')



#檔案下載
#('/serve/([^/]+)?', Serve_Handler)
class Serve_Handler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        #計算完畢後，進行Download_log寫入作業
        now = datetime.datetime.now().date()
        log_info = methods.load_log("Download_log",now)
        log_info.Usage_Bandwidth += blob_info.size
        log_info.put()
        #Bandwidth_log更新作業
        log_info = methods.load_log("Bandwidth_log","Quota")
        log_info.Download_Bandwidth -= blob_info.size
        log_info.put()
        self.send_blob(blob_info,save_as=True)


#檔案刪除
#('/delete', Delete_Handler)
class Delete_Handler(webapp2.RequestHandler):
    def post(self):
        try:
            keys = self.request.get("key")
            keys = keys.split(",")
            if len(keys) > 0 :
                for key in keys :
                    logging.info(key)
                    wrapper = Wrapper.get(key)
                    if wrapper:
                        if wrapper.blob:
                            blobstore.delete(wrapper.blob.key())
                        else:
                            self.response.out.write('No blob in wrapper')
                        db.delete(wrapper)
                self.redirect('/clouddrive')
            else:
                self.response.out.write('No wrapper for key %s' % key)
        except CapabilityDisabledError:
            self.response.out.write('Deleting disabled')


#GOOGLE帳戶登入
#('/account/([^/]+)?', Account_Handler)
class Account_Handler(webapp2.RequestHandler):
    def get(self, loginout_url):
        if users.get_current_user():
            self.redirect(users.create_logout_url('/' + loginout_url ))
        else:
            self.redirect(users.create_login_url('/' + loginout_url ))

#下載CSV
#('/csv', CSV_Handler)
class CSV_Handler(webapp2.RequestHandler):
    def post(self):
        log_Quota = None;
        select_csv = self.request.get("download_csv")
        self.response.headers['Content-Type'] = 'application/csv'
        if select_csv == "UBD" :
            Content_Disposition = 'attachment; filename=Upload_Bandwidth_Details ' +  str(datetime.datetime.now().date()) + '.csv'
            self.response.headers['Content-Disposition'] = Content_Disposition
            log_Quota = Upload_log.all().order('date')
        elif select_csv == "DBD" :
            Content_Disposition = 'attachment; filename=Download_Bandwidth_Details ' + str(datetime.datetime.now().date()) + '.csv'
            self.response.headers['Content-Disposition'] = Content_Disposition
            log_Quota = Download_log.all().order('date')
        writer = csv.writer(self.response.out)
        writer.writerow(["Date", "Usage(1)", "Usage(2)"])
        for log in log_Quota :
            writer.writerow([log.date,log.Usage_Bandwidth,countByte(log.Usage_Bandwidth)])