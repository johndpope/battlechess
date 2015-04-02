import sqlite3
import os


create = not os.path.exists('btch.db')

conn = sqlite3.connect('btch.db')
c = conn.cursor()
if create :
	# Create table
	c.execute('''CREATE TABLE users
				(id INTEGER PRIMARY KEY AUTOINCREMENT,
				login TEXT UNIQUE NOT NULL,
				pass TEXT NOT NULL,
				nbgames INTEGER DEFAULT 0,
				nbvictory INTEGER DEFAULT 0,
				nbdefeat INTEGER DEFAULT 0,
				streak_curr INTEGER DEFAULT 0,
				streak_max INTEGER DEFAULT 0,
				signup DATE DEFAULT (DATETIME('now')),
				active boolean DEFAULT 1)''')


	c.execute('''CREATE TABLE pastGames
				(id INTEGER PRIMARY KEY AUTOINCREMENT,
				idP1 INTEGER,
				idP2 INTEGER,
				file TEXT,
				date DATE DEFAULT (DATETIME('now')),
				winner INTEGER,
				FOREIGN KEY(idP1) REFERENCES users(id),
				FOREIGN KEY(idP2) REFERENCES users(id)
				)''')


	c.execute('''CREATE TABLE games
				(id INTEGER PRIMARY KEY AUTOINCREMENT,
				idP1 INTEGER,
				idP2 INTEGER,
				file TEXT,
				date DATE DEFAULT (DATETIME('now')),
				lastMove DATE DEFAULT NULL,
				turn CHAR DEFAULT 'w',
				FOREIGN KEY(idP1) REFERENCES users(id),
				FOREIGN KEY(idP2) REFERENCES users(id)
				)''')


	c.execute('''CREATE TABLE invitations
				(id INTEGER PRIMARY KEY AUTOINCREMENT,
				idP1 INTEGER,
				idP2 INTEGER,
				date DATE DEFAULT (DATETIME('now')),
				expirationDate DATE DEFAULT (DATETIME('now', '+5 days')),
				message TEXT DEFAULT '',
				FOREIGN KEY(idP1) REFERENCES users(id),
				FOREIGN KEY(idP2) REFERENCES users(id)
				)''')

	# Insert a row of data
	c.execute("INSERT INTO users (login, pass) VALUES ('Antoine', 'passAnt')")
	c.execute("INSERT INTO users (login, pass) VALUES ('Pol', 'passPol')")
	print c

	c.execute("INSERT INTO invitations (idP1, idP2) VALUES (1, 2)")
	# Save (commit) the changes
	conn.commit()

log = ('Antoine',)
c.execute('select pass from users where login=?', ('Antoine',))
c.execute('select id, pass from users where login=?', ('Pol',))
for p in c:
	print p



# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()