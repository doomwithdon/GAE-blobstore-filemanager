# -*- coding:UTF-8 -*
from random import choice
from django.utils import simplejson
from google.appengine.api import channel, memcache, users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
import logging


ANONYMOUS_IDS = set(range(1, 1000)) 
#對於陌生訪客來訪，對他們設置一個集合，從中對各個陌生訪客給予一個隨機編號

#python在定義副程式、函式時，是以def表示，如同void的道理
#廣播
def broadcast(message, tokens=None):
	if not tokens:
		tokens = memcache.get('tokens')
	if tokens:
		tokens.pop('_used_ids', None) 
		ids = set(tokens.values())
		for id in ids: 
			if isinstance(id, int):
				id = 'anonymous(%s)' % id
			channel.send_message(id, message)

#'/get_token', GetTokenHandler
#請從HTML的get_token對照，其功能為分配外來者匿名ID
class GetTokenHandler(webapp.RequestHandler):
	def get(self):
		#從快取記憶體取得"附記"或是空集合
		tokens = memcache.get('tokens') or {}
		#取得目前使用者名稱，並置入user中
		user = users.get_current_user()
		if user:
			#GOOGLE用戶，則取得你的email
			channel_id = id = user.email()
		else:
			#否則從堆疊中，取得一個匿名id
			#首先搜索匿名id有那些沒被使用過
			used_ids = tokens.get('_used_ids') or set()
			#第二步，從集合中找尋可以被使用的匿名id
			available_ids = ANONYMOUS_IDS - used_ids
			if available_ids:
				#將集合型態轉型為串列型態(亦為我們所熟知的陣列型態，是一個以非相同資料型態的物件元素陣列)
				available_ids = list(available_ids)
			else:
				self.response.out.write('')
				return
			#隨機從中選一個可用的匿名id
			id = choice(available_ids)
			#將匿名id註記為已被使用的id集合中
			used_ids.add(id)
			#更新"附記"的陣列
			tokens['_used_ids'] = used_ids
			#如果為陌生訪客，會給予一個隨機id表示您的身分
			channel_id = 'anonymous(%s)' % id
		#分配id之後，引導使用者進入聊天室
		token = channel.create_channel(channel_id)
		#將此id設定為被"附記"的名單中
		tokens[token] = id
		#將此儲存至快取記憶體
		memcache.set('tokens', tokens)
		self.response.out.write(token)
		logging.info("=============")

#'/del_token', ReleaseTokenHandler
#當客戶端使用refresh或是關閉網頁的動作時，要將"附記"(聊天室id)收回
class ReleaseTokenHandler(webapp.RequestHandler):
	def post(self):
		token = self.request.get('token')
		#
		if not token:
			return
		tokens = memcache.get('tokens')
		if tokens:
			id = tokens.get(token, '')
			if id:
				#isinstance為python的function，確認id是否為整數型態
				#一般而言，GOOGLE用戶其id組成必定為英文+數字組合，所以此對象排除在外
				#其目的是處理匿名id，將權限收走
				if isinstance(id, int):
					#對匿名id的權限收回處理
					used_ids = tokens.get('_used_ids')
					if used_ids:
						used_ids.discard(id)
						tokens['_used_ids'] = used_ids
					user_name = 'anonymous(%s)' % id
				else:
					#對GOOGLE用戶的權限收回處理
					user_name = id.split('@')[0]
				#從"附記"中刪除，del = delete
				del tokens[token]
				#更新快取記憶體
				memcache.set('tokens', tokens)
				message = user_name + ' has left the chat room.'
				message = simplejson.dumps(message)
				#將某人離開時，以廣播散播告知
				broadcast(message, tokens)

#'/open', OpenHandler
#外來者使用聊天室時的反應
class OpenHandler(webapp.RequestHandler):
	def post(self):
		#$.post('/open', {'token': token});中取得'token'其值
		token = self.request.get('token')
		if not token:
			return
		tokens = memcache.get('tokens')
		if tokens:
			id = tokens.get(token, '')
			if id:
				#python的function--isinstance類別判別，判斷是否為id是否為整數型態
				if isinstance(id, int):
					#唯有陌生訪客會被分配為編號表示身分
					user_name = 'anonymous(%s)' % id
				else:
					#如果是GOOGLE用戶，則取得信箱前的帳號名稱
					user_name = id.split('@')[0]
				message = user_name + u' has joined the chat room.'
				#將此訊息封裝至json中，新的訊息加入於舊的訊息其中
				message = simplejson.dumps(message)
				broadcast(message, tokens)

#'/post_msg', ReceiveHandler
#當客戶端要發送訊息
class ReceiveHandler(webapp.RequestHandler):
	def post(self):
		token = self.request.get('token')
		if not token:
			return
		message = self.request.get('content')
		if not message:
			return
		tokens = memcache.get('tokens')
		if tokens:
			id = tokens.get(token, '')
			if id:
				if isinstance(id, int):
					user_name = 'anonymous(%s)' % id
				else:
					user_name = id.split('@')[0]
				#message = "{'user_name': %s,'message': %s}" % (user_name, message)
				message = "%s:%s" % (user_name, message)
				message = simplejson.dumps(message)
				logging.info("=============")
				logging.info(message)
				if len(message) > channel.MAXIMUM_MESSAGE_LENGTH:
					return
				broadcast(message)