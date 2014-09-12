# -*- coding:UTF-8 -*-
from google.appengine.ext import webapp
import math

register = webapp.template.create_template_register()


@register.filter('countByte')
def countByte(value):
    value = int(value)
    if value < 1024 :
      return str(value) + "Byte"
    elif ( 1024 <= value ) and ( value < 1024**2 ) :
      return str(value / 1024) + "KB"
    elif ( 1024**2 <= value ) and ( value < 1024**3 ) :
      return str(value / (1024**2)) + "MB"
    elif 1024**3 <= value :
      return str(value / (1024**3)) + "GB"

@register.filter('blob_percentage')
def blob_percentage(value):
	value = float(value)
	#GAE的blobstore上限為5GB
	value = value / 5 /(1024**3)
	value = math.floor ( value * 10000 ) /100
	return str(value) + "%"

@register.filter('bandwidth_percentage')
def bandwidth_percentage(value):
  value = float(value)
  #GAE的bandwidth上限為1GB
  value = value / (1024**3)
  value = math.floor ( value * 10000 ) /100
  return str(value) + "%"