import sqlite3
from hashlib import sha1
import sys

users = {
	'vasia':'1234',
	'danny':'2345',
	'vander':'3456'
	}

conn = sqlite3.connect("rmcontest.db")
conn.execute('drop table if exists users')
conn.execute(
	"""
	create table users (
		user_id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT NOT NULL,
		hashed_password TEXT NOT NULL,
		time_last_attempt REAL,
		points INTEGER NOT NULL
	);	
	"""
)

for user in users:
	hashed_password = sha1(users[user].encode('ascii')).hexdigest()
	conn.execute('insert into users (username, hashed_password,time_last_attempt, points)'\
		' values ("%s", "%s", %s, %s);' % (user,hashed_password,0,0))

conn.commit()
conn.close()
