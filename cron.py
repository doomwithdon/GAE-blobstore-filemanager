# -*- coding:UTF-8 -*-
#引用"實例"
from models import *
import logging

class Quotas_Reset_Handler(webapp2.RequestHandler):
	def get(self):
		Bandwidth_reset = Bandwidth_log(key_name="Quota",
		                                Upload_Bandwidth = 1024**3,
		                                Download_Bandwidth =1024**3)
		Bandwidth_reset.put()