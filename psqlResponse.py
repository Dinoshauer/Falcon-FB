# -*- coding: utf-8 -*-
import psycopg2
import sys
import datetime
from collections import Counter


def getAllData(): 
	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object
		cur.execute('SELECT * FROM friends')

		# Gets all items in the query
		rows = cur.fetchall()

	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()
		return rows

def getAvgFriendCount():
	result = 0 
	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object
		cur.execute('SELECT AVG(friend_count) AS result FROM friends')

		# Gets all items in the query
		rows = cur.fetchone()
		result = rows[0]

	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()
		return result

def getGenderAmount(gender):
	data = getAllData()
	amount = 0.00
	for row in data:
		if row[4] == gender:
			amount += 1
	result = 100 * (amount/len(data))
	return result

def getMedian(gender):
	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object
		cur.execute("SELECT birthday_date FROM friends WHERE sex = '%s' AND birthday_date IS NOT NULL" % gender)

		# Gets all items in the query
		rows = cur.fetchall()
		result = []
		today = datetime.date.today().year
		for row in rows:
			# Convert the dates into years
			birthday = datetime.datetime.strptime(row[0], '%m/%d/%Y')
			age = today - birthday.year
			if age not in result:
				result.append(age)
	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()

		# Let's get that median!
		result = sorted(result)
		if len(result) % 2 == 1:
			return result[(len(result)+1/2-1)]
		else:
			lower = result[len(result)/2-1]
			upper = result[len(result)/2]
			return (float(lower+upper))/2

def getAvgFriendAge(gender = None):
	result = 0 
	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object
	 	if gender != None:
	 		cur.execute("SELECT birthday_date FROM friends WHERE sex = '%s' AND birthday_date IS NOT NULL" % gender)
	 	else:
			cur.execute("SELECT birthday_date FROM friends WHERE birthday_date IS NOT NULL")

		# Gets all items in the query
		rows = cur.fetchall()
		listResults = []
		today = datetime.date.today().year
		for row in rows:
			birthday = datetime.datetime.strptime(row[0], '%m/%d/%Y')
			age = today - birthday.year
			listResults.append(age)
		result = (sum(listResults)/len(listResults))
	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()
		return result

def getLocales(gender = None):
	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object
	 	if gender != None:
			cur.execute("SELECT locale FROM friends WHERE sex = '%s'" % gender)
		else:
			cur.execute("SELECT locale FROM friends")

		# Gets all items in the query
		rows = cur.fetchall()
		locale = {}
		for row in rows:
			# Convert the dates into years
			if row[0] not in locale:
				locale[row[0]] = 1
			else:
				locale[row[0]] = locale[row[0]] + 1

	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()
		return locale

def getDevices(gender = None):
	try:
		# Set up con with database name and username
		con = psycopg2.connect(database='FalconFB', user='k')
		cur = con.cursor() # Initialize the cursor object
		if gender != None:
			cur.execute("SELECT devices.uid, devices.hardware, devices.os FROM devices INNER JOIN friends ON devices.uid = friends.uid WHERE sex = '%s'" % gender)
		else:
			cur.execute("SELECT * FROM devices")

		# Gets all items in the query
		rows = cur.fetchall()
		devices = []
		for row in rows:
			devices.append(row)

	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()
		return devices

def countDevices(devices):
	result = {}
	allIOScount = 0
	allANDROIDcount = 0
	allIPADcount = 0
	allIPHONEcount = 0
	for device in devices:
		allIOScount += device.count('iOS')
		allANDROIDcount += device.count('Android')
		allIPADcount += device.count('iPad')
		allIPHONEcount += device.count('iPhone')
	result['iOS'] = allIOScount
	result['iPad'] = allIPADcount
	result['iPhone'] = allIPHONEcount
	result['Android'] = allANDROIDcount
	return result

def getDeviceUserAmount(gender = None):
	if gender != None:
		allDeviceUsers = getDevices(gender)
	else:
		allDeviceUsers = getDevices()
	allUsers = getAllData()
	amount = 0.00
	for row in allDeviceUsers:
		amount += 1
	result = 100 * (amount/len(allUsers))
	return result

def getPageData(gender = None): 
	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object
	 	if gender != None:
			cur.execute("SELECT pages.uid, pages.type FROM pages INNER JOIN friends ON pages.uid = friends.uid WHERE sex = '%s'" % gender)
	 	else:
			cur.execute("SELECT pages.uid, pages.type FROM pages INNER JOIN friends ON pages.uid = friends.uid")

		# Gets all items in the query
		rows = cur.fetchall()

	except psycopg2.DatabaseError, e:
		print 'Error: %s' % e
		sys.exit[1]
	finally:
		if con:
			con.close()
		return rows

def getAvgPageLikes(gender = None):
	allPages = getPageData(gender)
	allUsers = getAllData()
	result = float(len(allPages)/len(allUsers))
	return result


# print 'Printing all friends in list!'
#for row in getAllData():
#	print row
print
print '>> Average friend count pr. friend in the list: %.2f' % getAvgFriendCount()
print
print '>> Percentage of men in friend list: %.2f' % getGenderAmount('male')
print '>> Percentage of women in friend list: %.2f' % getGenderAmount('female')
print
print '>> Median age of all the men in the list: %.2f' % getMedian('male')
print '>> Median age of all the women in the list: %.2f' % getMedian('female')
print
print '>> Average age of all the people in the list: %d' % getAvgFriendAge()
print '>> Average age of all the men in the list: %d' % getAvgFriendAge('male')
print '>> Average age of all the women in the list: %d' % getAvgFriendAge('female')
print
print '>> Locale of all friends...'
maleLocales = getLocales()
for key, value in maleLocales.items():
	print '%s %d'.rjust(10) % (key, value)
print '>> Locale of male friends...'
maleLocales = getLocales('male')
for key, value in maleLocales.items():
	print '%s %d'.rjust(10) % (key, value)
print '>> Locale of female friends...'
maleLocales = getLocales('female')
for key, value in maleLocales.items():
	print '%s %d'.rjust(10) % (key, value)
print
# Device handling
devices = getDevices()
devicesMale = getDevices('male')
devicesFemale = getDevices('female')
print '>> Devices...'
print '>>>> Number of friends using...'
for key, value in countDevices(devices).items():
	print '%s %d'.rjust(10) % (key, value)
print '>>>> Number of men using...'
for key, value in countDevices(devicesMale).items():
	print '%s %d'.rjust(10) % (key, value)
print '>>>> Number of women using...'
for key, value in countDevices(devicesFemale).items():
	print '%s %d'.rjust(10) % (key, value)
print
print '>>>> Total amount of friends using a device with Facebook: %d friends' % len(devices)
cAll = Counter(elem[0] for elem in devices)
sumOfCounterAll = sum(value for key, value in cAll.iteritems() if value > 1)
print '>>>> Total amount of friend using multiple devices with Facebook: %d friends' % sumOfCounterAll
print '>>>> Percentage of all friends using Facebook with a device: %.2f' % getDeviceUserAmount()
print
print '>>>> Total amount of male friends using a device with Facebook: %d friends' % len(devicesMale)
cMale = Counter(elem[0] for elem in devicesMale)
sumOfCounterMale = sum(value for key, value in cMale.iteritems() if value > 1)
print '>>>> Total amount of friend using multiple devices with Facebook: %d friends' % sumOfCounterMale
print '>>>> Percentage of male friends using Facebook with a device: %.2f' % getDeviceUserAmount('male')
print
print '>>>> Total amount of female friends using a device with Facebook: %d friends' % len(devicesFemale)
cFemale = Counter(elem[0] for elem in devicesFemale)
sumOfCounterFemale = sum(value for key, value in cFemale.iteritems() if value > 1)
print '>>>> Total amount of friend using multiple devices with Facebook: %d friends' % sumOfCounterFemale
print '>>>> Percentage of female friends using Facebook with a device: %.2f' % getDeviceUserAmount('female')
print
print '>> Page type likes...'
pageData = getPageData()
malePageData = getPageData('male')
femalePageData = getPageData('female')
print '>>>> Average amount of pages liked pr. friend: %d pages' % getAvgPageLikes()
print '>>>> Average amount of pages liked pr. male friend: %d pages' % getAvgPageLikes('male')
print '>>>> Average amount of pages liked pr. female friend: %d pages' % getAvgPageLikes('female')
print '>>>> Pages liked by all genders (Top 20):'
c = Counter(elem[1] for elem in pageData)
for key, value in c.most_common(20):
	print '%s, %d'.rjust(11) % (key, value)
print '>>>> Pages liked by male friends (Top 5):'
c = Counter(elem[1] for elem in malePageData)
for key, value in c.most_common(5):
	print '%s, %d'.rjust(11) % (key, value)
print '>>>> Pages liked by female friends (Top 5):'
c = Counter(elem[1] for elem in femalePageData)
for key, value in c.most_common(5):
	print '%s, %d'.rjust(11) % (key, value)