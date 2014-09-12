# -*- coding:UTF-8 -*-
#!/usr/bin/env python

import os
import urllib
import webapp2


from google.appengine.api import users
from google.appengine.ext import blobstore, db, webapp
from google.appengine.ext.webapp import blobstore_handlers, template


#對模板註冊新功能
webapp.template.register_template_library('filterdir.customfilters')

# 在DB內創造一個資料表
class Wrapper(db.Model):
    user = db.UserProperty(auto_current_user=True)
    blob = blobstore.BlobReferenceProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)

#===後端服務 start ===

#上傳檔案
#('/upload', UploadHandler)
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:

            upload_files = self.get_uploads('file')
            if len(upload_files) > 0:
                blob_info = upload_files[0]
                Wrapper(blob=blob_info.key()).put()
            self.redirect('/')
        except CapabilityDisabledError:
            self.response.out.write('Uploading disabled')


#檔案下載
#('/serve/([^/]+)?', ServeHandler)
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


#檔案刪除
#('/delete', DeleteHandler)
class DeleteHandler(webapp2.RequestHandler):
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
#('/account', AccountHandler)
class AccountHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect(users.create_logout_url('/'))
        else:
            self.redirect(users.create_login_url('/'))

#===後端服務 end ===
#--------------------------------------------------------------------
#===前端服務 start ===

#('/', Home_Handler)
class Home_Handler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            loginout_url = users.create_logout_url('/')
        else:
            loginout_url = users.create_login_url('/')

        wrapper_total_size = 0
        for wrapper in Wrapper.all():
            wrapper_total_size += wrapper.blob.size
        values = {
            'user': users.get_current_user(),
            'users': users,
            'upload_url': blobstore.create_upload_url('/upload'),
            'wrappers': Wrapper.all(),
            'wrapper_total_size':wrapper_total_size,
            'startup_web':"home",
        }
        path = os.path.join(os.path.dirname(__file__), 'html','home.html')
        self.response.out.write(template.render(path, values))

#('/clouddrive', Clouddrive_Handler)
class Clouddrive_Handler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            loginout_url = users.create_logout_url('/')
        else:
            loginout_url = users.create_login_url('/')

        wrapper_total_size = 0
        for wrapper in Wrapper.all():
            wrapper_total_size += wrapper.blob.size

        values = {
            'user': users.get_current_user(),
            'users': users,
            'upload_url': blobstore.create_upload_url('/upload'),
            'wrappers': Wrapper.all(),
            'wrapper_total_size':wrapper_total_size,
            'startup_web':"clouddrive",
        }
        
        #1. 設置template與相對URL
        #我目前已經引用html/index.html為template，令html為執行基準位址
        #因此後面的base.html需要include都要從html之後來定義"相對URL"
        #ex: {%include "template/bootstrap-import-head.html" %}        

        #2. template不能與yaml重疊
        #我剛剛犯錯，在yaml將html/template上傳
        #雖然在PC端看起來正常，卻在mobile端顯示錯誤
        #顯然是個很大的錯誤!
        
        #path = os.path.join(os.path.dirname(__file__), 'yuntrun.htm')
        path = os.path.join(os.path.dirname(__file__), 'html','clouddrive.html')
        self.response.out.write(template.render(path, values))

class Test_Handler(webapp2.RequestHandler):
    def get(self):
        values = {
        }        
        path = os.path.join(os.path.dirname(__file__), 'html','yuntrun.htm')
        self.response.out.write(template.render(path, values))

#===前端服務 end ===  

#網址啟動
app = webapp2.WSGIApplication([
    #前端服務
    ('/', Home_Handler),
    ('/clouddrive', Clouddrive_Handler),
    ('/test1', Test_Handler),

    ('/account', AccountHandler),
    #後端服務
    ('/upload', UploadHandler),
    ('/serve/([^/]+)?', ServeHandler),
    ('/delete', DeleteHandler),
], debug=True)
