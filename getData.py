import facebook
import fbAuth
import time

def getFriends():
	graphApi = facebook.GraphAPI(fbAuth.get_token())

	# We need a list to hold our stuff
	friends = []

	# <3 FQL
	#q = 'SELECT uid,name,birthday_date,sex,locale,friend_count FROM user where uid IN (SELECT uid1 FROM friend WHERE uid2=me())'
	q = 'SELECT uid,name,birthday_date,sex,locale,friend_count,devices FROM user where uid IN (SELECT uid1 FROM friend WHERE uid2=me())'
	# Get the data from the returned object
	friendProfileInfo = graphApi.fql(q)

	print 'Getting friends with valid data available, please hold...'

	for friend in friendProfileInfo:
		#devices = str(friend['devices'])
		#friend['devices'] = devices
		bday = friend['birthday_date']
		try:
			time.strptime(str(friend['birthday_date']), '%m/%d/%Y')
			friends.append(friend)
		except ValueError:
			print('Invalid date! Adding friend to list without birthday')
			friend['birthday_date'] = None
			friends.append(friend)

	print 'Congratulations! All friends appended to friends list current amount of friends: %r!' % (len(friends))

	return friends

def getFriendsPages():
	graphApi = facebook.GraphAPI(fbAuth.get_token())

	# We need a list to hold our stuff
	pageData = []

	# <3 FQL
	q = "SELECT type, uid FROM page_fan WHERE uid IN (SELECT uid1 FROM friend WHERE uid2 = me())"

	# Get the data from the returned object
	friendProfileInfo = graphApi.fql(q)

	print 'Getting friends with valid page data available, please hold...'
	
	for page in friendProfileInfo:
		pageData.append(page)

	print 'Congratulations! All friends pages appended. Amount of pages: %r!' % (len(friendProfileInfo))

	return pageData