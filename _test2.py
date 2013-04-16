import getData
import dataWork

#print dataWork.insertDevices(getData.getFriends())

def prepareDevices(friends):
	friendsDevices = []
	for friend in friends:
		if friend['devices']:
			for device in friend['devices']:
				friendDict = {}
				friendDict['uid'] = friend['uid']
				if 'hardware' in device:
					friendDict['hardware'] = device['hardware']
				friendDict['os'] = device['os']

				friendsDevices.append(friendDict)
	return friendsDevices
for entry in prepareDevices(getData.getFriends()):
	print entry
# for entry in prepareDevices(getData.getFriends()):
# 	print 'Printing main object >>'
# 	print entry['devices']
# 	for device in entry['devices']:
# 		print 'Printing sub-object >>'
# 		print device
# 		print 'Printing "OS" from sub-object >>'
# 		print device['os']
# 		print 'Printing "Hardware" from sub-object >>'
# 		if 'hardware' in device:
# 			print device['hardware']