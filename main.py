# -*- coding:UTF-8 -*-
#!/usr/bin/env python

import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import blobstore, db, webapp
from google.appengine.ext.webapp import blobstore_handlers, template
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

#對模板註冊新功能
"""
register = template.Library()

@register.filter(name='countByte')
def countByte(value):
    if value < 1024 :
      return str(value) + "Byte"
    elif ( 1024 <= value ) and ( value < 1024**2 ) :
      return str(value / 1024) + "KB"
    elif ( 1024**2 <= value ) and ( value < 1024**3 ) :
      return str(value / (1024**2)) + "MB"
    elif 1024**3 <= value :
      return str(value / (1024**3)) + "GB"
"""
# 在DB內創造一個資料表
class Wrapper(db.Model):
    user = db.UserProperty(auto_current_user=True)
    blob = blobstore.BlobReferenceProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)


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


#('/', MainHandler)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            loginout_url = users.create_logout_url('/')
        else:
            loginout_url = users.create_login_url('/')
        values = {
            'user': users.get_current_user(),
            'users': users,
            'upload_url': blobstore.create_upload_url('/upload'),
            'wrappers': Wrapper.all(),
        }
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, values))


#GOOGLE帳戶登入
#('/account', AccountHandler)
class AccountHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect(users.create_logout_url('/'))
        else:
            self.redirect(users.create_login_url('/'))






#網址啟動
app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/account', AccountHandler),
                                  ('/upload', UploadHandler),
                                  ('/serve/([^/]+)?', ServeHandler),
                                  ('/delete', DeleteHandler),
                              ], debug=True)
