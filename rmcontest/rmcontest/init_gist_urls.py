import sqlite3

gist_urls = {
	1:"https://gist.github.com/vpatov/b061b868b7c3de041af1d338ca7372eb.js",
	3:"https://gist.github.com/vpatov/0a616d52a22ad7991e5ce2473897c75d.js",
	4:"https://gist.github.com/vpatov/4ab01a44d87c1a5541ef9a7c6b4cb8f7.js",
	6:"https://gist.github.com/vpatov/fcf9cb0a01a1f87086d2281f09ae0128.js",
	7:"https://gist.github.com/vpatov/80386dbe13b4dec318d767153a82ca6b.js"
	}

conn = sqlite3.connect("rmcontest.db")
conn.execute('drop table if exists gist_urls')
conn.execute(
	"""
	create table gist_urls (
		problem_num INTEGER PRIMARY KEY,
		gist_url TEXT NOT NULL
	);
	"""
)

for problem_num in gist_urls:
	conn.execute('insert into gist_urls (problem_num, gist_url)'\
		' values (%s, "%s");' % (problem_num,gist_urls[problem_num]))

conn.commit()
conn.close()
