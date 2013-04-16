import getData
import dataWork

print dataWork.insertFriends(getData.getFriends())
print 'Getting your friends page data, please hold. This may take a while.'
print dataWork.getPageLikes(getData.getFriendsPages())