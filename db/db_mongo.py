import pymongo
import config
import pymongo
import urllib.parse
from bson.objectid import ObjectId


class Database():
	def __init__(self):
		self.client = pymongo.MongoClient(config.MONGO_URI)
		self.db = self.client['DiaryBot']
		self.users = self.db['users']
		self.posts = self.db['posts']

	# Manage Posts

	def addPost(self, content, author_id, time_posted):
		post = {
			'content'		: content,
			'author_id'		: author_id,
			'time_posted'	: time_posted
		}
		self.posts.insert_one(post)

	def getPostByID(self, id):
		post = self.posts.find_one({'_id' : ObjectId(id)})
		post['id'] = post['_id']
		return post

	def getRandomPost(self):
		post = list(self.posts.aggregate([{'$sample': { 'size': 1 } }]))[0]
		return {"id" : post['_id'], "content" : post['content'], "author_id" : post['author_id'], "time_posted" : post['time_posted']}

	def deletePost(self, id):
		self.posts.delete_one({'_id' : ObjectId(id)})

	def postCount(self):
		return self.posts.count()

	# Manage Users

	def addUser(self, user_id):
		user = {
			'user_id'		: user_id,
			'is_admin'		: 0,
		}
		self.users.insert_one(user)

	def addAdmin(self, user_id):
		self.user = {
			'user_id'		: user_id,
			'is_admin'		: 1,
		}
		self.users.insert_one(user)

	def removeUser(self, user_id):
		self.users.delete_one({'user_id' : user_id})

	def removeAdmin(self, user_id):
		self.users.delete_one({'user_id' : user_id})

	def isUser(self, user_id):
		entry = self.users.find_one({'user_id' : user_id})
		return (not entry == None)

	def isAdmin(self, user_id):
		entry = self.users.find_one({'user_id' : user_id})
		if (entry == None):
			return 0
		return entry['is_admin']

	def getUsers(self):
		rows = self.users.find({})
		return rows