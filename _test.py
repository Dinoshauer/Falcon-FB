friends = [{'friend_count': None, 'uid': 737112358, 'locale': 'en_US', 'sex': 'female', 'birthday_date': '07/31/1988', 'name': 'Nanna Louise List Stensvig'}]
# Build the table based on the keywords from the FQL
count = 0
table = 'CREATE TABLE friends (id serial PRIMARY KEY, '
for name, value in friends[0].items():
	count = count + 1
	if count < len(friends[0]):
		if type(value) == str:
			table += '{0} VARCHAR(100), '.format(name)
		elif type(value) == int:
			table += '{0} INT, '.format(name)
	else:
		if type(value) == str:
			table += '{0} VARCHAR(100))'.format(name)
		elif type(value) == int:
			table += '{0} INT)'.format(name)
print table

# Build the string for the INSERT statement
count = 0
tableLayout = 'INSERT INTO ('
for name, value in friends[0].items():
	count = count + 1
	if count < len(friends[0]):
		tableLayout += '{0}, '.format(name)
	else:
		tableLayout += '{0}) VALUES ('.format(name)
count = 0
for name, value in friends[0].items():
	count = count + 1
	if count < len(friends[0]):
		tableLayout += '%({0})r, '.format(name)
	else:
		tableLayout += '%({0})r)'.format(name)
print tableLayout
