import facebook
import fbAuth
import time

def getFriendsPages():
	graphApi = facebook.GraphAPI(fbAuth.get_token())

	# We need a list to hold our stuff
	friends = []

	# <3 FQL
	q = "SELECT type, uid FROM page_fan WHERE uid IN (SELECT uid1 FROM friend WHERE uid2 = me())"

	# Get the data from the returned object
	friendProfileInfo = graphApi.fql(q)

	print 'Getting friends with valid page data available, please hold...'

	print 'Congratulations! All friends pages appended. Amount of pages: %r!' % (len(friendProfileInfo))

	return friendProfileInfo

getFriendsPages()