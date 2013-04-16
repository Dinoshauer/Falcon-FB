# -*- coding: utf-8 -*-
import psycopg2
import sys

def prepareDevices(friends):
	friendsDevices = []
	for friend in friends:
		if friend['devices']:
			for device in friend['devices']:
				friendDict = {}
				friendDict['uid'] = friend['uid']
				if 'hardware' in device:
					friendDict['hardware'] = device['hardware']
				else:
					friendDict['hardware'] = None
				friendDict['os'] = device['os']

				friendsDevices.append(friendDict)
	return friendsDevices

def getPageLikes(pages):
	con = None
	result = False

	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object

	 	cur.execute("DROP TABLE IF EXISTS pages")
	 	cur.execute("CREATE TABLE pages (uid VARCHAR(100), type VARCHAR(100))")

	 	q = "INSERT INTO pages (uid, type) VALUES (%(uid)s, %(type)s)"

	 	cur.executemany(q, pages)
	 	con.commit()

	 	result = True

	except psycopg2.DatabaseError, e:
		if con:
			con.rollback() # Roll back any changes made on error

		print 'Error: %s' % e
		
	finally:
		if con:
			con.close()
		if result:
			return 'Your friends\' pagedata has been inserted in the database.'

def insertFriends(friends):
	# Initialize con as None, else we might get an error if something bad happens
	con = None
	result = False

	try:
	 	# Set up con with database name and username
	 	con = psycopg2.connect(database='FalconFB', user='k')
	 	cur = con.cursor() # Initialize the cursor object

	 	# Drop the table if it exists
	 	cur.execute("DROP TABLE IF EXISTS friends")
	 	# Create the table
		#cur.execute('CREATE TABLE IF NOT EXISTS friends(id serial PRIMARY KEY, uid VARCHAR(100), name VARCHAR(100), birthday_date VARCHAR(10), sex VARCHAR(10), locale VARCHAR(10), friend_count INT)') # Execute a statement
		cur.execute('CREATE TABLE friends(id serial PRIMARY KEY, uid VARCHAR(100), name VARCHAR(100), birthday_date VARCHAR(10), sex VARCHAR(10), locale VARCHAR(10), friend_count INT)') # Execute a statement
		
	 	q = 'INSERT INTO friends (uid, name, birthday_date, sex, locale, friend_count) VALUES (%(uid)s, %(name)s, %(birthday_date)s, %(sex)s, %(locale)s, %(friend_count)s)'
		
		# Device work
		cur.execute("DROP TABLE IF EXISTS devices")
		cur.execute('CREATE TABLE devices(uid VARCHAR(100), hardware VARCHAR(50), os VARCHAR(50))')
		qDevices = 'INSERT INTO devices (uid, hardware, os) VALUES (%(uid)s, %(hardware)s, %(os)s)'
		cur.executemany(qDevices, prepareDevices(friends))
		print 'Your friends devices have been inserted in the database.'

	 	cur.executemany(q, friends)
	 	# Same as ExecuteNonQuery()(?) pretty much I think
		con.commit()

		# Set the result boolean to true, so we know nothing's happened
		result = True

	except psycopg2.DatabaseError, e:
		if con:
			con.rollback() # Roll back any changes made on error

		print 'Error: %s' % e
		
	finally:
		if con:
			con.close()
		if result:
			return 'Your friends have been inserted in the database.'