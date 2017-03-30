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
	"""Hi {user_name}! You've correctly signed up on your group {group_name}.
From now on you'll have 10 daily points to give away to your fellow group members.
	""",
        'zero-points-to-give':
        """Sorry, but you do not have any points left.
        """,
	'no-points-left':
	"""Sorry, but you only have {points_left} point{plural_p_l} left.
	""", 
	'points-received':
	"""{user_name} has {points_received} point{plural_p_r}!
	""",
	'my-points':
	"""You have received {points_received} point{plural_p_r}!
And {points_left} point{plural_p_l} left for today.
	"""
}
