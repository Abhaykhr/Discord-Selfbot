import discord
import datetime
import random
import requests
import json
import os
import sys
from datetime import datetime
from PythonGists import PythonGists
from discord.ext import commands
from cogs.utils.checks import *

'''Dump messages'''

class DumpThemMessages:
	def __init__(self, bot):
		self.bot = bot
		config = load_config()
		self.bot_prefix = config["bot_identifier"]
			
	@commands.command(pass_context=True)
	async def archive(self,ctx,silent=False):
		"""Archives every channel in a guild to text files.
		
		Usage: >archive [silent]
		[silent] - boolean whether or not to print status messages in the chat (will not suppress errors) (Optional, defaults to False)
		"""
		await ctx.message.delete()
		guildnamesafe = ctx.message.guild.name
		illegalchars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
		for i in illegalchars: # because some guilds will put slashes and things
			guildnamesafe = guildnamesafe.replace(i, '_')
		timenow = str(int(time.time()))
		if not os.path.isdir('guild_archives'):
			os.mkdir('guild_archives')
		if not os.path.isdir('guild_archives/' + guildnamesafe + '_' + timenow):
			os.mkdir('guild_archives/' + guildnamesafe + '_' + timenow)
		if not silent:
			await ctx.message.channel.send(self.bot.bot_prefix + 'Archiving guild...')
		try:
			for c in ctx.message.guild.channels:
				try:
					if not type(c) is discord.TextChannel:
						raise discord.LoginFailure
					print('Dumping ' + c.name + '...          ', end="")
					sys.stdout.flush()
					channelnamesafe = c.name
					for i in illegalchars: # because some guilds will put slashes and things
						channelnamesafe = channelnamesafe.replace(i, '_')
					messages = []
					async for message in c.history(limit=999999999999):
						messages.append("{} [{}] <{}#{}_{}> {}\n".format(time.mktime(message.created_at.timetuple()), message.created_at.ctime(), message.author.name, message.author.discriminator, message.author.id, message.content).encode()) # thankee https://stackoverflow.com/a/29298798
					messages2 = sorted(messages)
					file = open('guild_archives/' + guildnamesafe + '_' + timenow + '/' + guildnamesafe + '_' + channelnamesafe + '__' + str(c.id) + '.txt', 'wb+')
					file.write(('Archival of channel #' + c.name + ' [ID:' + str(c.id) + '] in guild ' + ctx.message.guild.name + ' [ID:' + str(ctx.message.guild.id) + '] on ' + str(datetime.now()) + '\n\n').encode('utf-8')) # thankee https://stackoverflow.com/a/5877368 and https://stackoverflow.com/q/7585435
					for line in messages2:
						file.write(line)
					print('Finished dumping.')
					file.close()
				except discord.errors.Forbidden:
					print('Could not dump! [Reason: Forbidden]')
				except discord.LoginFailure:
					print('Did not dump ' + c.name + '... [Reason: NotTextChannel]')
				except:
					print('Could not dump! [Reason: Unknown!]')
					raise
			print('Finished archiving guild ' + ctx.message.guild.name + '!')
			if not silent:
				await ctx.message.channel.send(self.bot.bot_prefix + 'Finished archiving guild!')
		except:
			await ctx.message.channel.send(self.bot.bot_prefix + 'An error has occured!')
			raise
			
def setup(bot):
	bot.add_cog(DumpThemMessages(bot))
	