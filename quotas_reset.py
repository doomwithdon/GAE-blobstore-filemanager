#引用"實例"
from models import *
import logging
Bandwidth_reset = Bandwidth_log(key_name=key_name,
                                Upload_Bandwidth = 1024**3,
                                Download_Bandwidth =1024**3)
Bandwidth_reset.put()
logging.info("＊＼／＼／＼／＼／＼／＼／＼／＼／＼／＼／＼／＼／＊")
logging.info("＊＝＝＝＝＝＝＝＝＝＝ＯＫ＝＝＝＝＝＝＝＝＝＝＝＝＊")
logging.info("＊＼／＼／＼／＼／＼／＼／＼／＼／＼／＼／＼／＼／＊")