import sqlite3
from hashlib import sha1
import sys

users = {
	'vasia':'1234',
	'danny':'2345',
	'vander':'3456'
	}

conn = sqlite3.connect("rmcontest.db")
for user in users:
	hashed_password = sha1(users[user].encode('ascii')).hexdigest()
	conn.execute('insert into users (username, hashed_password,time_last_attempt, points)'\
		' values ("%s", "%s", %s, %s);' % (user,hashed_password,0,0))

conn.commit()
conn.close()
