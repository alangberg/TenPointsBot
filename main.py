# TenPoints_Bot - Main
# Nicolas Luce - 03/2017

import telepot
import sys, time, pprint, datetime
import commandHandlers as cm
from commandHandlers import *
from helpers import *

def handle(message):
	print 'Message received...'
	pprint.pprint(message)

	try:
		
		print cm.saved_date
		print datetime.date.today()

		if 'data' in message:
			return
		if (on_user_joins(BOT, message) or
			on_user_lefts(BOT, message)):
			return
		if cm.saved_date < datetime.date.today():
			reset_points(BOT, message)
			cm.main_db.collection.update_one({'_id':1}, 
					{'$currentDate': {'date': {'$type':'date'}}})
			cm.saved_date = cm.main_db.get_document({'_id':1})['date'].date()
		if isCommand(message):
			commandHandler(BOT, message, getCommand(message), getCommandParameters(message))
			return
		elif (not is_private(message) and 
			'text' in message and 
			'reply_to_message' in message):
			points = 0
			if (message['text'].startswith('+') and 
				message['text'].split('+')[1].isdigit()):
				points = int(message['text'].split('+')[1])

			if (message['text'].startswith('-') and 
				message['text'].split('-')[1].isdigit()):
				points = int(message['text'].split('-')[1])
				points = -1*int(message['text'].split('-')[1])
			
			print "POINT REQUEST RECEIVED: " + str(points)
			if abs(points) > 0 and abs(points) <= 10:
				addPoints(BOT, message, points, message['from']['id'], message['reply_to_message']['from']['id'])
		return

	except telepot.exception.MigratedToSuperGroupChatError, e:
		cm.main_db.update_post(message['id'], 'id', e[2]['parameters']['migrate_to_chat_id'])
	except Exception as e:
		raise
	
print 'Starting Bot...'
TOKEN = sys.argv[1]
DB_USER_NAME = sys.argv[2]
DB_PASSWORD = sys.argv[3]

# cm.MAIN_DICCONARY = {}
# save_obj(cm.MAIN_DICCONARY, "MAIN_DICCONARY")
cm.main_db = db(DB_USER_NAME, DB_PASSWORD)
# cm.main_db.insert_document({'_id':1})
# cm.main_db.collection.update_one({'_id':1}, 
# 		{'$currentDate': {'date': {'$type':'date'}}})

cm.saved_date = cm.main_db.get_document({'_id':1})['date'].date()

BOT = telepot.Bot(TOKEN)

BOT.message_loop(handle)
print 'Listening'

while 1:
	time.sleep(10)
