import discord
from discord.ext import commands
import config
import datetime

if(config.DATABASE == "MONGO"):
	from db.db_mongo import Database
else:
	from db.db_sqlite import Database

class DiaryCog(commands.Cog, name='Diary'):

	def __init__(self, bot):
		self.bot = bot
		self.db = Database()

	@commands.command()
	async def count(self, ctx):
		"""Get the number of posts"""
		await ctx.send("There are {} ping messages".format(self.db.postCount()))

	@commands.command()
	async def submit(self, ctx):
		"""Submit a new post"""
		if(not (self.db.isUser(ctx.message.author.id) or (ctx.message.guild.owner.id == ctx.message.author.id))):
			await ctx.send("Only authorized users can submit posts")
			return
		submission = ctx.message.content[8:]
		self.db.addPost(submission, ctx.message.author.id, ctx.message.created_at.timestamp())

	def createEmbed(self, post):
		embed = discord.Embed(
			title = "Post #{}".format(post['id']),
			description = post['content'],)
		embed.add_field(
			name = "Submited By",
			value = self.bot.get_user(post['author_id']).display_name,
			inline = True)
		embed.add_field(
			name = "Date Submitted",
			value = datetime.datetime.utcfromtimestamp(post['time_posted']).replace(microsecond=0),
			inline = True)
		return embed;

	@commands.command()
	async def read(self, ctx, id):
		"""Read a post by post number"""
		post = self.db.getPostByID(id)
		await ctx.send(embed=self.createEmbed(post))

	@commands.command()
	async def random(self, ctx):
		"""Get a random post"""
		if self.db.postCount() == 0:
			await ctx.send("There aren't any posts yet. Try adding one with {}submit".format(config.COMMAND_SYMBOL))
			return
		post = self.db.getRandomPost()
		await ctx.send(embed=self.createEmbed(post))

	@commands.command()
	async def delete(self, ctx, id):
		"""Delete a post by post number"""
		if(not (self.db.isAdmin(ctx.message.author.id) or (ctx.message.guild.owner.id == ctx.message.author.id))):
			await ctx.send("Only admins can delete posts")
			return
		print(self.db.deletePost(id))

def setup(bot):
    bot.add_cog(DiaryCog(bot))