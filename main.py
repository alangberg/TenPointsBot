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
			cm.saved_date = datetime.date.today()
			save_obj(cm.saved_date, 'saved_date')
			reset_points(BOT, message)
		if isCommand(message):
			commandHandler(BOT, message, getCommand(message), getCommandParameters(message))
			return
		elif (not is_private(message) and 
			message['text'].startswith('+') and 
			message['text'].split('+')[1].isdigit() and
			'reply_to_message' in message):

			points = int(message['text'].split('+')[1])
			print "POINT REQUEST RECEIVED: " + str(points)
			if points > 0 and points <= 10:
				addPoints(BOT, message, points, message['from']['id'], message['reply_to_message']['from']['id'])
		return

	except Exception as e:
		raise
	
print 'Starting Bot...'
TOKEN = sys.argv[1]

# cm.MAIN_DICCONARY = {}
# save_obj(cm.MAIN_DICCONARY, "MAIN_DICCONARY")
cm.MAIN_DICCONARY = load_obj('MAIN_DICCONARY')

# cm.saved_date = datetime.date.today();
# save_obj(cm.saved_date, 'saved_date')
cm.saved_date = load_obj('saved_date')

BOT = telepot.Bot(TOKEN)

BOT.message_loop(handle)
print 'Listening'

while 1:
	time.sleep(10)
