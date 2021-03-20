import discord
from discord.ext import commands

import os
import requests
import random

class MemeCog(commands.Cog, name='Meme Generator'):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def memeify(self, ctx, topText, bottomText, img = None):
		"""Memify an image"""
		if(img == None):
			imgUrl = ctx.message.attachments[0].url
		else:
			imgUrl = img
		response = requests.get("https://api.memegen.link/images/custom/{}/{}.png?background={}".format(topText, bottomText, imgUrl), allow_redirects=True)
		fname = "meme-{}.png".format(random.randint(1, 999))
		open(fname, 'wb').write(response.content)
		await ctx.send(file=discord.File(fname))
		os.remove(fname)


def setup(bot):
	bot.add_cog(MemeCog(bot))