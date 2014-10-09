# -*- coding:UTF-8 -*-
from google.appengine.ext import webapp
import math
import logging

register = webapp.template.create_template_register()


@register.filter('countByte')
def countByte(value):
    value = float(value)
    unit  = ""
    if value < 1024 :
      unit = "Byte"
    elif ( 1024 <= value ) and ( value < 1024**2 ) :
      value = value / (1024)
      unit = "KB"
    elif ( 1024**2 <= value ) and ( value < 1024**3 ) :
      value = value / (1024**2)
      unit = "MB"   
    elif 1024**3 <= value :
      value = value / (1024**3)
      unit = "GB"
    return str( math_chop(value,"normal") ) + unit

@register.filter('percentage')
def percentage(value,select):
  value = float(value)  
  value = value / (1024**3)  #先將數值轉換至GB為單位
  if select =="Blob" :
    value = value / 5 #blobstore上限為5GB
  elif select =="bandwidth" :
    value = value / 1 #bandwidth上限為1GB
  value =  math_chop(value,"percentage")
  return str(value) + "%"

#辦別檔案類型，MIME規則如下:
#Text：用於標準化地表示的文本信息，文本消息可以是多種字符集和或者多種格式的；
#Multipart：用於連接消息體的多個部分構成一個消息，這些部分可以是不同類型的數據；
#Application：用於傳輸應用程序數據或者二進制數據；
#Message：用於包裝一個E-mail消息；
#Image：用於傳輸靜態圖片數據；
#Audio：用於傳輸音頻或者音聲數據；
#Video：用於傳輸動態影像數據，可以是與音頻編輯在一起的視頻數據格式。
@register.filter('Content_Type')
def Content_Type(mime):
  if (mime.find("image") >= 0 ) :
    return "fa fa-file-image-o"
  elif (mime.find("video") >= 0):
    return "fa fa-file-video-o"
  elif (mime.find("audio") >= 0):
    return "fa fa-file-audio-o"
  elif (mime.find("text") >= 0):
    return "fa fa-file-text"
  elif (mime.find("application") >= 0):
    if (mime.find("octet-stream") >= 0):
      return "fa fa-file-archive-o"
    elif (mime.find("pdf") >= 0):
      return "fa fa-file-pdf-o" 
    elif ( (mime.find("sheet") >= 0) or (mime.find("spread") >= 0) or (mime.find("excel") >= 0)):
      return "fa fa-file-excel-o"
    elif (mime.find("word") >= 0):
      return "fa fa-file-word-o"
    elif (mime.find("javascript") >= 0):
      return "fa fa-file-code-o"    
    else :
      return "fa fa-file-o"
  else :
    return "fa fa-file-o"

#無條件捨去，只留到小數第二位
def math_chop(value,select):
  if select == "normal" :
    return math.floor ( value * 100 ) /100
  elif select == "percentage" :
    return math.floor ( value * 10000 ) /100

