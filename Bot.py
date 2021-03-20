import discord
from discord.ext import commands
import config

cogs = ['cogs.Diary', 'cogs.Administration', 'cogs.Bitcoin', 'cogs.Memes']

intents = discord.Intents.default()
intents.members=True

bot = commands.Bot(config.COMMAND_SYMBOL, description=config.DESCRIPTION, intents = intents)

if __name__ == '__main__':
	for c in cogs:
		bot.load_extension(c)

@bot.event
async def on_ready():
	print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

bot.run(config.DISCORD_TOKEN)