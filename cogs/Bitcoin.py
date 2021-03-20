import discord
from discord.ext import commands

import requests

class BitcoinCog(commands.Cog, name='Cryptocurrency'):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def bitcoin(self, ctx):
		"""Get the current bitcoin price"""
		response = requests.get("https://api.coinlore.net/api/ticker/?id=80")
		data = response.json()[0]
		embed = discord.Embed(
			title='Bitcoin Price', 
			description='${}'.format(data['price_usd']), 
			)
		embed.set_footer(text='Data from coinlore.com')
		await ctx.send(embed=embed)

	@commands.command()
	async def ethereum(self, ctx):
		"""Get the current ethereum price"""
		response = requests.get("https://api.coinlore.net/api/ticker/?id=80")
		data = response.json()[0]
		embed = discord.Embed(
			title='Ethereum Price', 
			description='${}'.format(data['price_usd']), 
			)
		embed.set_footer(text='Data from coinlore.com')
		await ctx.send(embed=embed)

	@commands.command()
	async def monero(self, ctx):
		"""Get the current ethereum price"""
		response = requests.get("https://api.coinlore.net/api/ticker/?id=28")
		data = response.json()[0]
		embed = discord.Embed(
			title='Monero Price', 
			description='${}'.format(data['price_usd']), 
			)
		embed.set_footer(text='Data from coinlore.com')
		await ctx.send(embed=embed)

	@commands.command()
	async def dogecoin(self, ctx):
		"""Get the current ethereum price"""
		response = requests.get("https://api.coinlore.net/api/ticker/?id=2")
		data = response.json()[0]
		embed = discord.Embed(
			title='Dogecoin Price', 
			description='${}'.format(data['price_usd']), 
			)
		embed.set_footer(text='Data from coinlore.com')
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(BitcoinCog(bot))