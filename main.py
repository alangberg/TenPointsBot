# TenPoints_Bot - Main
# Nicolas Luce - 03/2017

import telepot
import sys, time, pprint
from commandHandlers import commandHandler, on_user_joins
from helpers import *

def handle(message):
	print 'Message received...'
	pprint.pprint(message)

	try:
		if 'data' in message:
			return
		if on_user_joins(bot, msg):
			return
		if isCommand(message):
			commandHandler(BOT, message, getCommand(message), getCommandParameters(message))
			return
		elif (not is_private(message) and 
			message['text'].startswith('+') and 
			message['text'].split('+')[1].isdigit() and
			'reply_to_message' in message):

			points = int(message['text'].split('+')[1])
			if points > 0 and points < 10:
				addPoints(bot, message, points, message['reply_to_message']['chat']['id'], message['reply_to_message']['from']['id'])
		return

	except Exception as e:
		raise
	
print 'Starting Bot...'
TOKEN = sys.argv[1]

MAIN_DICCONARY = {}
save_obj(MAIN_DICCONARY, 'MAIN_DICCONARY')
MAIN_DICCONARY = load_obj('MAIN_DICCONARY')

BOT = telepot.Bot(TOKEN)

BOT.message_loop(handle)
print 'Listening'

while 1:
	time.sleep(10)
