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

#無條件捨去，只留到小數第二位
def math_chop(value,select):
  if select == "normal" :
    return math.floor ( value * 100 ) /100
  elif select == "percentage" :
    return math.floor ( value * 10000 ) /100
   

#測試參數代入是否有效
@register.filter('cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return str(value) + "+" +arg