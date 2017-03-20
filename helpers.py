# Helper Functions
# Nicolas Luce - 03/2017

import pickle, os.path

def is_group(msg):
	return msg['chat']['type'] == 'group' or msg['chat']['type'] == 'supergroup'

def is_private(msg):
	return msg['chat']['type'] == 'private'

def isMember(bot, uId, gId):
	status = bot.getChatMember(gId, uId)['status']
	if status == 'member' or status == 'administrator' or status == 'creator':
		return True
	return False

def isCommand(msg):
	return (('entities' in msg) and (msg['entities'][0]['type'] == 'bot_command'))

def getCommand(msg):
	if not isCommand(msg):
		raise SimpleMessageException({'error':'Message parameter is not a command', 'msg':msg})
	return msg['text'].split()[0]

def getCommandParameters(msg):
	if not isCommand(msg):
		raise SimpleMessageException({'error':'Message parameter is not a command', 'msg':msg})

	command = getCommand(msg)
	return msg['text'].split(command, 1)[1].strip()

def save_obj(obj, name):
	path = os.getcwd()
	with open(path + '/'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	path = os.getcwd()
	with open(path + '/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

# Excepction

class SimpleMessageException(Exception):
	pass