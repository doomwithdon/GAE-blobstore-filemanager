# -*- coding:UTF-8 -*-
import webapp2

from models import *
import logging

import urllib

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
            if len(upload_files) > 0:   
                logging.info(upload_files)
                for blob_info in upload_files :
                    blob_key = blob_info.key() #註冊key
                    blob_filename = str(blob_info.filename) #取得filename 
                    blob_content_type = str(blob_info.content_type) #取得檔案類型
                    logging.info(blob_content_type)
                    Wrapper(blob=blob_key,
                            filename=blob_filename,
                            content_type=blob_content_type).put()
            self.redirect('/clouddrive')
        except CapabilityDisabledError:
            self.response.out.write('Uploading disabled')



#檔案下載
#('/serve/([^/]+)?', Serve_Handler)
class Serve_Handler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        #logging.info(blob_info.filename)
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
#('/account', Account_Handler)
class Account_Handler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect(users.create_logout_url('/clouddrive'))
        else:
            self.redirect(users.create_login_url('/clouddrive'))