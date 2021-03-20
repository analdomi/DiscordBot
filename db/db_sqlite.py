import sqlite3

class Database:
	def __init__(self):
		self.conn = sqlite3.connect("data.db")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER, is_admin INTEGER)")
		self.cur.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, content TEXT, author_id INTEGER, time_posted INTEGER)")
		self.conn.commit()

	def __del__(self):
		self.conn.close()

	# Manage Posts

	def addPost(self, content, author_id, time_posted):
		self.cur.execute("INSERT INTO posts(content, author_id, time_posted) VALUES (?,?,?)",(content,author_id,time_posted))
		self.conn.commit()

	def getPostByID(self, id):
		self.cur.execute("SELECT * FROM posts WHERE id=?", (id))
		post = self.cur.fetchone()
		return {"id" : post[0], "content" : post[1], "author_id" : post[2], "time_posted" : post[3]}

	def getRandomPost(self):
		self.cur.execute("SELECT * FROM posts ORDER BY RANDOM() LIMIT 1")
		post = self.cur.fetchone()
		return {"id" : post[0], "content" : post[1], "author_id" : post[2], "time_posted" : post[3]}

	def deletePost(self, id):
		self.cur.execute("DELETE FROM posts WHERE id=?", (id))
		self.conn.commit()

	def postCount(self):
		self.cur.execute("SELECT * FROM posts")
		rows = self.cur.fetchall()
		return len(rows)

	# Manage Users

	def addUser(self, user_id):
		self.cur.execute("INSERT INTO users(user_id, is_admin) VALUES (?, ?)",(user_id, 0))
		self.conn.commit()

	def addAdmin(self, user_id):
		self.cur.execute("INSERT INTO users(user_id, is_admin) VALUES (?, ?)",(user_id, 1))
		self.conn.commit()

	def removeUser(self, user_id):
		self.cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
		self.conn.commit()

	def removeAdmin(self, user_id):
		self.cur.execute("UPDATE users SET is_admin=1 WHERE user_id=?",(user_id,))
		self.conn.commit()

	def isUser(self, user_id):
		self.cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
		row = self.cur.fetchone()
		return (not row == None)

	def isAdmin(self, user_id):
		self.cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
		row = self.cur.fetchone()
		if(row == None):
			return 0
		return row[1]

	def getUsers(self):
		self.cur.execute("SELECT * FROM users")
		rows = self.cur.fetchall()
		posts = [];
		for r in rows:
			posts.append({"id" : r[0], "user_id" : r[1], "is_admin" : r[2]})
		return posts