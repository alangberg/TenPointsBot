# Messages for TenPoints_Bot
# Nicolas Luce - 03/2017

messages = {
	'welcome':
	"""Hi! My name is TenPoints_Bot, 
I'll assign 10 daily points to each member of the group so you may grant them between you.
To do so please use the /signup command so I know you are a member of this group.
In any case use /help or /info to know more about my functionalities.""",
	'help':
	"""
	""",
	'sign-up':
	"""Hi {user_name}! You've correctly signed up.
From now on you'll have 10 daily points to give away to your fellow group members.
	""",
	'no-points-left':
	"""Sorry, but you only have {points_left} points left.
	""", 
	'points-received':
	"""{user_name} has {points_received} points!
	""",
	'my-points':
	"""You have received {points_received} points!
And {points_left} points left for today.
	"""
}
