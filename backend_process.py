# -*- coding:UTF-8 -*-
import webapp2

from models import Wrapper,Bandwidth_log

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
                    blob_key = blob_info.key() #取得key
                    blob_filename = str(blob_info.filename) #取得filename 
                    blob_content_type = str(blob_info.content_type) #取得檔案類型
                    logging.info(blob_content_type)             

                    Wrapper(blob=blob_info,
                            filename=blob_filename,
                            content_type=blob_content_type).put()
            self.redirect('/clouddrive')
        except CapabilityDisabledError:
            self.response.out.write('Uploading disabled')
# -*- coding:UTF-8 -*-

from google.appengine.api import users
from google.appengine.ext import blobstore

#檔案下載
#('/serve/([^/]+)?', Serve_Handler)
class Serve_Handler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


#檔案刪除
#('/delete', Delete_Handler)
class Delete_Handler(webapp2.RequestHandler):
    def post(self):
        try:
            key = self.request.get("key")
            wrapper = Wrapper.get(key)
            if wrapper:
                if wrapper.blob:
                    blobstore.delete(wrapper.blob.key())
                else:
                    self.response.out.write('No blob in wrapper')
                db.delete(wrapper)
                self.redirect('/')
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