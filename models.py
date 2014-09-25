# -*- coding:UTF-8 -*-
from google.appengine.ext import db,blobstore

# 在DB內創造一個資料表
class Wrapper(db.Model):
    #1.上傳者
    user = db.UserProperty(auto_current_user=True)
    #2.需要blobkey才可以參考blobstore
    blob = blobstore.BlobReferenceProperty(required=True)
    #3.檔名
    filename = db.StringProperty()
    #4.檔案類型
    content_type = db.StringProperty()
    #5.上傳時間
    date = db.DateTimeProperty(auto_now_add=True)

class Bandwidth_log(db.Model):
    Upload_Bandwidth = db.IntegerProperty()
    Download_Bandwidth = db.IntegerProperty()
    def Bandwidth_init(self) :
        #調用父類別
        super(Bandwidth_log,self).put()

