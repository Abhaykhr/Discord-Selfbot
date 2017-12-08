import discord
import time
import os
from discord.ext import commands

'''Display Hidden Channels'''

class SneakyStuff:

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def hchan(self, ctx):
        """Show hidden channels"""
        await ctx.message.delete()
        if type(ctx.channel) == discord.channel.DMChannel:
            return await ctx.send(self.bot.bot_prefix + "This command *obviously* doesn't work in a DM, you peasant.")
        channels = ""
        nechannels = ""
        hidden = 0
        total = len(ctx.guild.text_channels)
        embed = discord.Embed(title="Hidden channels in {}".format(ctx.message.guild))
        for x in ctx.guild.text_channels:
            if not x.permissions_for(ctx.author).read_messages:
                channels += "**#{}**".format(x.name)
                nechannels += "#{}".format(x.name)
                if x.topic == "None" or not x.topic:
                    channels += "\n\n"
                    nechannels += "\n\n"
                else:
                    channels += " - {}\n\n".format(x.topic)
                    nechannels += " - {}\n\n".format(x.topic)
                hidden += 1
        embed.description = channels
        footer = "{} out of {} channels are hidden".format(hidden, total)
        embed.set_footer(text=footer)
        if not channels:
            await ctx.send(self.bot.bot_prefix + "There are no channels you cannot see!")
        else:
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.send("```{}\n\n{}```".format(nechannels, footer))
    @commands.command(pass_context=True)
    async def dump(self, ctx, limit):
        """Dump messages."""
        await ctx.message.delete()	
        channel2 = ctx.message.channel
        chanName = channel2.name
        server2 = ctx.message.guild
        serverstr = server2.name
        dateNow = time.strftime("%d-%m-%y")
        timeNow = time.strftime("%H%M%S")
        filename = dateNow + "_" + serverstr + "_" + "#" + chanName + timeNow
        currentchanneldir1 = "message_dump/" + serverstr + "/" + "Message_Logs/"        
        if not os.path.isdir("message_dump/" + serverstr + "/"):
            os.mkdir("message_dump/" + serverstr + "/")
        if not os.path.isdir(currentchanneldir1):
            os.mkdir(currentchanneldir1)
        with open(currentchanneldir1 + filename.rsplit('.', 1)[0] + ".txt", "w+", encoding="utf-8") as f:
                    async for message in ctx.message.channel.history(limit=int(limit)):
                        f.write("<{} at {} on {}> {}\n".format(message.author.name, message.created_at.strftime('%d %b %Y'), message.created_at.strftime('%H:%M:%S'), message.content))
    @commands.command(pass_context=True)
    async def mde(self, ctx, limit, channelId):
        """Dump messages without sending the message in the server."""
        await ctx.message.delete()
        chanId = int (channelId)		
        chan = self.bot.get_channel(chanId) 
        chanName = chan.name
        dateNow = time.strftime("%d-%m-%y")
        timeNow = time.strftime("%H%M%S")
        serverr = chan.guild
        serverstr = serverr.name
        filename = dateNow + "_" + serverstr + "_" + "#" + chanName + timeNow
        currentchanneldir = "message_dump/" + serverstr + "/" + "Message_Logs/"
        if not os.path.isdir("message_dump/" + serverstr + "/"):
            os.mkdir("message_dump/" + serverstr + "/")
        if not os.path.isdir(currentchanneldir):
            os.mkdir(currentchanneldir)
        with open(currentchanneldir + filename.rsplit('.', 1)[0] + ".txt", "w+", encoding="utf-8") as f:
                    async for message in chan.history(limit=int(limit)):
                        f.write("<{} at {} on {}> {}\n".format(message.author.name, message.created_at.strftime('%d %b %Y'), message.created_at.strftime('%H:%M:%S'), message.content))
    @commands.group(pass_context=True)
    async def hcd(self, ctx):
        """Dump hidden channels."""
        await ctx.message.delete()	
        channel2 = ctx.message.channel
        channel = channel2.name
        server2 = ctx.message.guild
        serverstr = server2.name
        dateNow = time.strftime("%d-%m-%y")
        timeNow = time.strftime("%H%M%S")
        filenamechans = dateNow + "_" + serverstr + timeNow
        currentchanneldir = "message_dump/" + serverstr + "/" + "Hidden_Channels/"
        nechannels = ""
        hidden = 0
        for x in ctx.guild.text_channels:
            if not x.permissions_for(ctx.author).read_messages:
                nechannels += "#{}".format(x.name)
                if x.topic == "None" or not x.topic:
                    nechannels += "\n\n"
                else:
                    nechannels += " - {}\n\n".format(x.topic)
                hidden += 1
        if not os.path.isdir("message_dump/" + serverstr + "/"):
            os.mkdir("message_dump/" + serverstr + "/")
        if not os.path.isdir(currentchanneldir):
            os.mkdir(currentchanneldir)
        with open(currentchanneldir + filenamechans.rsplit('.', 1)[0] + ".txt", "w+", encoding="utf-8") as f:
                    if hidden > 0:
                        f.write(nechannels)
                    else:
                        f.write("No hidden Channels")
    @commands.command(pass_context=True)
    async def hce(self, ctx, channelId):
        """Show hidden channels externally. Just get a random channel id, it will work, trust me."""
        await ctx.message.delete()
        chanId = int (channelId)
        chan = self.bot.get_channel(chanId)
        guildObj = chan.guild
        channels = ""
        nechannels = ""
        hidden = 0
        total = len(chan.guild.text_channels)
        embed = discord.Embed(title="Hidden channels in {}".format(guildObj))
        for x in chan.guild.text_channels:
            if not x.permissions_for(ctx.author).read_messages:
                channels += "**#{}**".format(x.name)
                nechannels += "#{}".format(x.name)
                if x.topic == "None" or not x.topic:
                    channels += "\n\n"
                    nechannels += "\n\n"
                else:
                    channels += " - {}\n\n".format(x.topic)
                    nechannels += " - {}\n\n".format(x.topic)
                hidden += 1
        embed.description = channels
        footer = "{} out of {} channels are hidden".format(hidden, total)
        embed.set_footer(text=footer)
        if not channels:
            await ctx.send(self.bot.bot_prefix + "There are no channels you cannot see!")
        else:
            try:
                await ctx.send(embed=embed)
            except:
                await ctx.send("```{}\n\n{}```".format(nechannels, footer))
        
def setup(bot):
    bot.add_cog(SneakyStuff(bot))
