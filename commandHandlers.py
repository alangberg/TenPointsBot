# Command handlers
# Nicolas Luce - 03/2017

import operator

from helpers import *
from messages import messages

global MAIN_DICCONARY
global saved_date

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

def on_user_lefts(bot, msg):
	if ('left_chat_member' in msg and 
		'username' in msg['left_chat_member'] and 
		msg['left_chat_member']['username'] == bot.getMe()['username']):
		del MAIN_DICCONARY[msg['chat']['id']]
		save_obj(MAIN_DICCONARY, "MAIN_DICCONARY")
		return True
	return False

def commandHandler(bot, msg, command, parameters= None):
	if bot.getMe()['username'] in command: command = command.split('@' + bot.getMe()['username'])[0]
	if command == '/start': command_start(bot, msg)
	elif command == '/signup': command_signup(bot, msg)
	elif command == '/mypoints': command_mypoints(bot, msg)
	elif command == '/top5': command_top5(bot, msg)
	elif command == '/help': command_start(bot, msg)
	elif command == '/info': command_start(bot, msg)

	return

def command_start(bot, msg):
	if is_private(msg):
		bot.sendMessage(msg['chat']['id'], messages['welcome'], reply_to_message_id=msg['message_id'])
	else:
		group_id = msg['chat']['id']
		if not group_id in MAIN_DICCONARY:
			MAIN_DICCONARY[group_id] = {}
			save_obj(MAIN_DICCONARY, "MAIN_DICCONARY")
		bot.sendMessage(msg['chat']['id'], messages['welcome'], reply_to_message_id=msg['message_id'])
	return

def command_signup(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		user_id = msg['from']['id']
		if group_id in MAIN_DICCONARY:
			if not user_id in MAIN_DICCONARY[group_id]:
				name = msg['from']['first_name']
				if 'last_name' in msg['from']:
					name += ' ' + msg['from']['last_name']
				
				MAIN_DICCONARY[group_id][user_id] = {'points_received':0, 'points_left':10, 'user_name':name}
				save_obj(MAIN_DICCONARY, "MAIN_DICCONARY")
				print MAIN_DICCONARY[group_id][user_id]
				bot.sendMessage(group_id, messages['sign-up'].format(user_name=msg['from']['first_name']), reply_to_message_id=msg['message_id'])
			else:
				return
		else:
			command_start(bot, msg)
			return

def command_mypoints(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		user_id = msg['from']['id']
		if group_id in MAIN_DICCONARY:
			if user_id in MAIN_DICCONARY[group_id]:
				points_received = MAIN_DICCONARY[group_id][user_id]['points_received']
				points_left = MAIN_DICCONARY[group_id][user_id]['points_left']
				bot.sendMessage(group_id, messages['my-points'].format(points_received=points_received, points_left=points_left), reply_to_message_id=msg['message_id'])
			else:
				return
		else:
			command_start(bot, msg)
			return

def command_top5(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		if group_id in MAIN_DICCONARY:
			top5 = [(x[1]['user_name'], x[1]['points_received']) for x in sorted(MAIN_DICCONARY[group_id].iteritems(), key=lambda (k,v): v['points_received'])][:5]
			top5.reverse()
			message = "Top 5:\n"
			for member in top5:
				message += member[0] + ': ' + str(member[1]) + '\n' 
			bot.sendMessage(group_id, message)

def addPoints(bot, msg, points, sender, receiver):
	group_id = msg['chat']['id']
	if group_id in MAIN_DICCONARY:
		if (sender in MAIN_DICCONARY[group_id] and 
			receiver in MAIN_DICCONARY[group_id] and
			sender != receiver):
			print "POINTS REQUESTED: " + str(points)
			print "POINTS LEFT:" + str(MAIN_DICCONARY[group_id][sender]['points_left'])
			if points <= MAIN_DICCONARY[group_id][sender]['points_left']:
				MAIN_DICCONARY[group_id][receiver]['points_received'] += points
				MAIN_DICCONARY[group_id][sender]['points_left'] -= points

				save_obj(MAIN_DICCONARY, 'MAIN_DICCONARY')

				bot.sendMessage(group_id, messages['points-received'].format(user_name=msg['reply_to_message']['from']['first_name'], points_received=MAIN_DICCONARY[group_id][receiver]['points_received']))
			else:
				bot.sendMessage(group_id, messages['no-points-left'].format(points_left=MAIN_DICCONARY[group_id][sender]['points_left']), reply_to_message_id=msg['message_id'])
		else:
			if (sender in MAIN_DICCONARY[group_id] and 
				receiver not in MAIN_DICCONARY[group_id]):
					bot.sendMessage(group_id, "That user has not sign up.")

			print "USER NOT SIGN UP"
			return
	else:
		print "GROUP NOT SIGN UP"
		return

def reset_points(bot, msg):
	print MAIN_DICCONARY
	for group in MAIN_DICCONARY:
		print group
		for member in MAIN_DICCONARY[group]:
			print MAIN_DICCONARY[group][member]
			MAIN_DICCONARY[group][member]['points_left'] = 10
	bot.sendMessage(msg['chat']['id'], "Points restarted.")