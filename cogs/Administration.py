import discord
from discord.ext import commands
import config

if(config.DATABASE == "MONGO"):
	from db.db_mongo import Database
else:
	from db.db_sqlite import Database

class AdministrationCog(commands.Cog, name='Administration'):

	def __init__(self, bot):
		self.bot = bot
		self.db = Database()

	@commands.command()
	async def setUser(self, ctx, user: discord.User):
		"""Add a user"""
		if(not(self.db.isAdmin(ctx.message.author.id)) or (ctx.message.guild.owner.id == ctx.message.author.id)):
			print("Only admins can use this command")
			return
		if (user.id == ctx.message.guild.owner.id):
			return
		self.db.addUser(user.id)

	@commands.command()
	async def setAdmin(self, ctx, user: discord.User):
		"""Add an admin"""
		if(not ctx.message.guild.owner.id == ctx.message.author.id):
			print("Only the server owner can use this command")
			return
		if (user.id == ctx.message.guild.owner.id):
			return
		self.db.addAdmin(user.id)

	@commands.command()
	async def removeUser(self, ctx, user: discord.User):
		"""Remove a user"""
		if(not(self.db.isAdmin(ctx.message.author.id)) or (ctx.message.guild.owner.id == ctx.message.author.id)):
			print("Only admins can use this command")
			return
		if(user.id == ctx.message.guild.owner.id):
			await ctx.send("Cannot remove server owner".format(self.bot.get_user(ctx.message.guild.owner.id).display_name))
			return
		await ctx.send("Cannot remove server owner")
		self.db.removeUser(user.id)

	@commands.command()
	async def removeAdmin(self, ctx, user: discord.User):
		"""Remove an admin, but they will still be a user"""
		if(not ctx.message.guild.owner.id == ctx.message.author.id):
			print("Only the server owner can use this command")
			return
		if(not(self.db.isAdmin(ctx.message.author.id)) or (ctx.message.guild.owner.id == ctx.message.author.id)):
			print("Only admins can use this command")
			return
		self.db.removeAdmin(user.id)

	@commands.command()
	async def isUser(self, ctx, user: discord.User):
		"""Check if someone is allowed to make posts"""
		if(user.id == ctx.message.guild.owner.id):
			await ctx.send("{} is the server owner".format(self.bot.get_user(ctx.message.guild.owner.id).display_name))
			return
		if(self.db.isUser(user.id)):
			await ctx.send("{} is a user".format(self.bot.get_user(user.id).display_name))
		else:
			await ctx.send("{} is not a user".format(self.bot.get_user(user.id).display_name))

	@commands.command()
	async def isAdmin(self, ctx, user: discord.User):
		"""Check if someone is an admin"""
		if (user.id == ctx.message.guild.owner.id):
			await ctx.send("{} is the server owner".format(self.bot.get_user(ctx.message.guild.owner.id).display_name))
			return
		if(self.db.isAdmin(user.id)):
			await ctx.send("{} is an admin".format(self.bot.get_user(user.id).display_name))
		else:
			await ctx.send("{} is not an admin".format(self.bot.get_user(user.id).display_name))


	@commands.command()
	async def getUsers(self, ctx):
		"""See a list of all authorized users"""
		users = self.bot.get_user(ctx.message.guild.owner.id).display_name + " Owner\n"
		for u in self.db.getUsers():
			users += self.bot.get_user(u['user_id']).display_name
			if(u['is_admin']):
				users += " Admin\n"
			else:
				users += "\n"

		embed = discord.Embed(
			title = "Users",
			description = users)

		await ctx.send(embed=embed)

	@commands.command()
	async def getAdmins(self, ctx):
		"""See a list of admins"""
		admins = self.bot.get_user(ctx.message.guild.owner.id).display_name + " Owner\n"
		for u in self.db.getUsers():
			if(u['is_admin']):
				admins += self.bot.get_user(u['user_id']).display_name + "\n"

		embed = discord.Embed(
			title = "Admins",
			description = admins)

		await ctx.send(embed=embed)

	@commands.command()
	async def kick(self, ctx, user: discord.User):
		"""Kick a user from the server"""
		if(not(self.db.isAdmin(ctx.message.author.id)) or (ctx.message.guild.owner.id == ctx.message.author.id)):
			print("Only admins can use this command")
			return
		if (self.db.isAdmin(user.id)):
			return
		await bot.kick(userName)

def setup(bot):
    bot.add_cog(AdministrationCog(bot))