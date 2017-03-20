# Command handlers
# Nicolas Luce - 03/2017

from helpers import *
from messages import messages

global MAIN_DICCONARY

def on_user_joins(bot, msg):
	if ('new_chat_member' in msg and 
		'username' in msg['new_chat_member'] and 
		msg['new_chat_member']['username'] == bot.getMe()['username']):

		group_id = msg['chat']['id']
		MAIN_DICCONARY[group_id] = {}
		save_obj(MAIN_DICCONARY, "MAIN_DICCONARY")
		command_start(bot, msg)
		return True
	return False

def commandHandler(bot, msg, command, parameters= None):
	if bot.getMe()['username'] in command:
		command = command.split('@' + bot.getMe()['username'])[0]
	print command
	if command == '/start': 
		command_start(bot, msg)
	elif command == '/signUp': 
		command_signUp(bot, msg)
	# elif command == '/mygroup': command_mygroup(bot, msg)
	# elif command == '/deleteme': command_deleteme(bot, msg)
	# elif command == '/refresh': command_refresh(bot, msg) 
	# elif command == '/burn': command_burn(bot, msg)
	# elif command == '/setburn': command_setburn(bot, msg, parameters)
	# elif command == '/help' or command == '/info': command_info_help(bot, msg)

	return

def command_start(bot, msg):
	if is_private(msg):
		bot.sendMessage(msg['chat']['id'], messages['welcome'], reply_to_message_id=msg['message_id'])
	else:
		bot.sendMessage(msg['chat']['id'], messages['welcome'], reply_to_message_id=msg['message_id'])
	return

def command_signUp(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		user_id = msg['from']['id']
		if group_id in MAIN_DICCONARY:
			if not user_id in MAIN_DICCONARY[group_id]:
				MAIN_DICCONARY[group_id][user_id] = {'points_received':0, 'points_left':10}
				bot.sendMessage(group_id, messages['sign-up'].format(user_name=msg['from']['first_name']), reply_to_message_id=msg['message_id'])
			else:
				return
		else:
			command_start(bot, msg)
			return

def addPoints(bot, msg, points, sender, receiver):
	group_id = msg['chat']['id']
	if group_id in MAIN_DICCONARY:
		if sender in MAIN_DICCONARY[group_id] and receiver in MAIN_DICCONARY[group_id]:
			if points <= MAIN_DICCONARY[group_id][sender]['points_left']:
				MAIN_DICCONARY[group_id][receiver]['points_received'] += points
				MAIN_DICCONARY[group_id][sender]['points_left'] -= points

				save_obj(MAIN_DICCONARY, 'MAIN_DICCONARY')

				bot.sendMessage(group_id, messages['points-received'].format(user_name=msg['reply_to_message']['from']['first_name'], points_received=MAIN_DICCONARY[group_id][receiver]['points_received']))
			else:
				bot.sendMessage(group_id, messages['no-points-left'].format(points_left=MAIN_DICCONARY[group_id][sender]['points_left']), reply_to_message_id=msg['message_id'])
		else:
			return
	else:
		return
