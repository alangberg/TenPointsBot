# Command handlers
# Nicolas Luce - 03/2017

import telepot
import operator, pprint, pymongo
from helpers import *
from messages import messages
from database import db

global main_db
global saved_date

def formated_message(msg_key, **kwargs): 
	if msg_key == 'no-points-left' and kwargs['points_left'] == 0:
		msg_key = 'zero-points-to-give'

	if 'points_received' in kwargs:
		kwargs['plural_p_r'] = "" if kwargs['points_received'] == 1 else "s"
	if 'points_left' in kwargs:
		kwargs['plural_p_l'] = "" if kwargs['points_left'] == 1 else "s"

	return messages[msg_key].format(**kwargs)

def on_group_migrate(bot, msg):
	if ('migrate_from_chat_id' in msg):
		docs = main_db.find_documents()

		for group in docs:
			main_db.update_post({'group_id':group['group_id']}, 
				'group_id', msg['migrate_from_chat_id'])
		return True
	
	if ('migrate_to_chat_id' in msg):
		docs = main_db.find_documents()

		for group in docs:
			main_db.update_post({'group_id':group['group_id']}, 
				'group_id', msg['migrate_to_chat_id'])
		return True

	return False


def on_user_joins(bot, msg):
	if ('new_chat_member' in msg and 
		'username' in msg['new_chat_member'] and 
		msg['new_chat_member']['username'] == bot.getMe()['username']):

		command_start(bot, msg)
		return True
	return False

def on_user_lefts(bot, msg):
	if ('left_chat_member' in msg and 
		'username' in msg['left_chat_member'] and 
		msg['left_chat_member']['username'] == bot.getMe()['username']):
		main_db.delete_documents({'group_id':msg['chat']['id']})
		
		return True
	return False

def is_user_on_group(group_id, user_id):
	doc = main_db.get_document(
			{'$and':[
				{'user_id':user_id},
				{'group_id':group_id}
			]}
		)
	return (doc != None)

def commandHandler(bot, msg, command, parameters= None):
	if bot.getMe()['username'] in command: command = command.split('@' + bot.getMe()['username'])[0]
	if command == '/start': command_start(bot, msg)
	elif command == '/signup': command_signup(bot, msg)
	elif command == '/mypoints': command_mypoints(bot, msg)
	elif command == '/top5': command_top5(bot, msg)
	elif command == '/help': command_start(bot, msg)
	elif command == '/info': command_start(bot, msg)
    	elif command == '/bottom5': command_bottom5(bot, msg)

	return

def command_start(bot, msg):
	if is_private(msg):
		bot.sendMessage(msg['chat']['id'], messages['welcome'], reply_to_message_id=msg['message_id'])
	else:
		bot.sendMessage(msg['chat']['id'], messages['welcome'], reply_to_message_id=msg['message_id'])
	return


def command_signup(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		user_id = msg['from']['id']
		if not is_user_on_group(group_id, user_id):
			print 'is on group'
			name = msg['from']['first_name']
			if 'last_name' in msg['from']:
				name += ' ' + msg['from']['last_name']

			new_post = {
				'group_id':group_id,
				'user_id':user_id,
				'points_received':0,
				'points_left':10,
				'user_name':name
			}

			main_db.insert_document(new_post)

			bot.sendMessage(user_id, messages['sign-up'].format(user_name=msg['from']['first_name'], group_name=msg['chat']['title']))
		else:
			return

def command_mypoints(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		user_id = msg['from']['id']
		if is_user_on_group(group_id, user_id):
			doc = main_db.get_document(
					{'$and':[
						{'group_id':group_id},
						{'user_id':user_id}
					]})

			points_received = doc['points_received']
			points_left = doc['points_left']
			form_msg = formated_message('my-points',**{'points_received':points_received, 'points_left':points_left})
			bot.sendMessage(group_id, form_msg, reply_to_message_id=msg['message_id'])
		else:
			return

def command_top5(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		top5 = main_db.find_documents({'group_id':group_id}).sort('points_received', pymongo.DESCENDING)

		message = "Top 5:\n"
		for member in top5[:5]:
			message += member['user_name'] + ': ' + str(member['points_received']) + '\n' 
		bot.sendMessage(group_id, message)

def command_bottom5(bot, msg):
	if not is_private(msg):
		group_id = msg['chat']['id']
		bottom5 = main_db.find_documents({'group_id':group_id}).sort('points_received', pymongo.ASCENDING)

		message = "Bottom 5:\n"
		for member in bottom5[:5]:
			message += member['user_name'] + ': ' + str(member['points_received']) + '\n' 
		bot.sendMessage(group_id, message)

def addPoints(bot, msg, points, sender, receiver):
	group_id = msg['chat']['id']
	if (is_user_on_group(group_id, sender) and 
		is_user_on_group(group_id, receiver) and
		sender != receiver):

		sender_points_left = main_db.get_document(
			{'$and':[
				{'group_id':group_id},
				{'user_id':sender}
			]})['points_left']

		if abs(points) <= sender_points_left:
			
			receiver_points_received = main_db.get_document(
			{'$and':[
				{'group_id':group_id},
				{'user_id':receiver}
			]})['points_received']

			receiver_points_received += points
			sender_points_left -= abs(points)

			main_db.update_post(
				{'$and':[
					{'group_id':group_id},
					{'user_id':receiver}
				]},
				'points_received', receiver_points_received)

			main_db.update_post(
				{'$and':[
					{'group_id':group_id},
					{'user_id':sender}
				]},
				'points_left', sender_points_left)				

			# bot.sendMessage(group_id, messages['points-received'].format(user_name=msg['reply_to_message']['from']['first_name'], points_received=receiver_points_received))
		else:
					form_msg = formated_message('no-points-left', **{'points_left':sender_points_left})
					bot.sendMessage(group_id, form_msg, reply_to_message_id=msg['message_id'])
	else:
		# if (is_user_on_group(group_id, sender) and 
		# 	not is_user_on_group(group_id, receiver)):
		# 		# bot.sendMessage(group_id, "That user has not sign up.")
		print "USER NOT SIGNED UP"
		return
	
def reset_points(bot, msg):
	try:
		docs = main_db.find_documents()

		groups = set()

		for group in docs:
			if 'points_left' in group:
				main_db.update_post(
					{'$and':[
						{'group_id':group['group_id']},
						{'user_id':group['user_id']}
					]}, 'points_left', 10)
				groups.add(group['group_id'])

		for group_id in groups:
			send_reset_message(bot, group_id)

def send_reset_message(bot, group_id):
	try:
		bot.sendMessage(group_id, "Points restarted.")
	except telepot.exception.MigratedToSupergroupChatError, e:
		main_db.update_post({'group_id':group_id}, 'group_id', e[2]['parameters']['migrate_to_chat_id'])
		print "MigrateToSupergroupChatError: group " + str(group_id) + "uptaded to " + str(e[2]['parameters']['migrate_to_chat_id'])
