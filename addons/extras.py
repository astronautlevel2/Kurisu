import datetime
import discord
import os
import random
import string
from discord.ext import commands

class Extras:
    """
    Extra things.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    prune_key = "nokey"

    @commands.command()
    async def kurisu(self, aliases=['about']):
        """About Kurisu"""
        embed = discord.Embed(title="Kurisu", color=discord.Color.green())
        embed.set_author(name="Started by 916253, maintained by ihaveahax")
        embed.set_thumbnail(url="http://i.imgur.com/hjVY4Et.jpg")
        embed.url = "https://github.com/nh-server/Kurisu"
        embed.description = "Kurisu, the Nintendo Homebrew Discord bot!"
        await self.bot.say("", embed=embed)

    @commands.command()
    async def membercount(self):
        """Prints the member count of the server."""
        await self.bot.say("{} has {:,} members!".format(self.bot.server.name, self.bot.server.member_count))

    @commands.has_permissions(ban_members=True)
    @commands.command(hidden=True)
    async def embedtext(self, *, text):
        """Embed content."""
        await self.bot.say(embed=discord.Embed(description=text))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def estprune(self, days=30):
        """Estimate count of members that would be pruned based on the amount of days. Staff only."""
        if days > 30:
            await self.bot.say("Maximum 30 days")
            return
        if days < 1:
            await self.bot.say("Minimum 1 day")
            return
        msg = await self.bot.say("I'm figuring this out!".format(self.bot.server.name))
        count = await self.bot.estimate_pruned_members(server=self.bot.server, days=days)
        await self.bot.edit_message(msg, "{:,} members inactive for {} day(s) would be kicked from {}!".format(count, days, self.bot.server.name))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def activecount(self, days=30):
        """Shows the number of members active in the past amount of days. Staff only."""
        if days > 30:
            await self.bot.say("Maximum 30 days")
            return
        if days < 1:
            await self.bot.say("Minimum 1 day")
            return
        msg = await self.bot.say("I'm figuring this out!".format(self.bot.server.name))
        count = await self.bot.estimate_pruned_members(server=self.bot.server, days=days)
        if days == 1:
            await self.bot.edit_message(msg, "{:,} members were active today in {}!".format(self.bot.server.member_count-count, self.bot.server.name))
        else:
            await self.bot.edit_message(msg, "{:,} members were active in the past {} days in {}!".format(self.bot.server.member_count-count, days, self.bot.server.name))


    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True)
    async def prune30(self, ctx, key=""):
        """Prune members that are inactive for 30 days. Staff only."""
        if self.bot.pruning > 0:
            await self.bot.say("Pruning is already in progress.")
            return
        if key != self.prune_key:
            if key != "":
                await self.bot.say("That's not the correct key.")
            self.prune_key = ''.join(random.sample(string.ascii_letters, 8))
            await self.bot.say("Are you sure you want to prune members inactive for 30 days?\nTo see how many members get kicked, use `.estprune`.\nTo confirm the prune, use the command `.prune30 {}`.".format(self.prune_key))
            return
        self.prune_key = ''.join(random.sample(string.ascii_letters, 8))
        await self.bot.say("Starting pruning!")
        count = await self.bot.prune_members(self.bot.server, days=30)
        self.bot.pruning = count
        await self.bot.send_message(self.bot.mods_channel, "{:,} are currently being kicked from {}!".format(count, self.bot.server.name))
        msg = "👢 **Prune**: {} pruned {:,} members".format(ctx.message.author.mention, count)
        await self.bot.send_message(self.bot.modlogs_channel, msg)

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def disableleavelogs(self):
        """DEBUG COMMAND"""
        self.bot.pruning = True
        await self.bot.say("disable")

    @commands.has_permissions(manage_nicknames=True)
    @commands.command()
    async def enableleavelogs(self):
        """DEBUG COMMAND"""
        self.bot.pruning = False
        await self.bot.say("enable")

    @commands.command(name="32c3")
    async def _32c3(self):
        """Console Hacking 2015"""
        await self.bot.say("https://www.youtube.com/watch?v=bZczf57HSag")

    @commands.command(name="33c3")
    async def _33c3(self):
        """Nintendo Hacking 2016"""
        await self.bot.say("https://www.youtube.com/watch?v=8C5cn_Qj0G8")

    @commands.command(name="34c3")
    async def _34c3(self):
        """Console Security - Switch"""
        await self.bot.say("https://www.youtube.com/watch?v=Ec4NgWRE8ik")

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True)
    async def dumpchannel(self, ctx, channel_name, limit=100):
        """Dump 100 messages from a channel to a file."""
        channel = ctx.message.channel_mentions[0]
        await self.bot.say("Dumping {} messages from {}".format(limit, channel.mention))
        os.makedirs("#{}-{}".format(channel.name, channel.id), exist_ok=True)
        async for message in self.bot.logs_from(channel, limit=limit):
            with open("#{}-{}/{}.txt".format(channel.name, channel.id, message.id), "w") as f:
                f.write(message.content)
        await self.bot.say("Done!")

    @commands.command(pass_context=True, hidden=True)
    async def togglechannel(self, ctx, channelname):
        """Enable or disable access to specific channels."""
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if channelname == "elsewhere":
            if self.bot.elsewhere_role in author.roles:
                await self.bot.remove_roles(author, self.bot.elsewhere_role)
                await self.bot.send_message(author, "Access to #elsewhere removed.")
            else:
                await self.bot.add_roles(author, self.bot.elsewhere_role)
                await self.bot.send_message(author, "Access to #elsewhere granted.")
        elif channelname == "eventchat":
            if self.bot.eventchat_role in author.roles:
                await self.bot.remove_roles(author, self.bot.eventchat_role)
                await self.bot.send_message(author, "Access to #eventchat granted.")
            else:
                await self.bot.add_roles(author, self.bot.eventchat_role)
                await self.bot.send_message(author, "Access to #eventchat granted.")
        else:
            await self.bot.send_message(author, "{} is not a valid toggleable channel.".format(channelname))


    # helper method to ensure certain commands can only be ran in bot.botcmds_channel
    async def verify_botcmds(self, ctx):
        if ctx.message.channel != self.bot.botcmds_channel:
            await self.bot.send_message(ctx.message.author, "`{}` can only be ran in {}".format(ctx.prefix + ctx.invoked_with, self.bot.botcmds_channel.mention))
            await self.bot.delete_message(ctx.message)
            return False
        return True
    
    @commands.command(pass_context=True)
    async def rainbow(self, ctx):
        """Colorful"""
        if not await self.verify_botcmds(ctx): return
        month = datetime.date.today().month
        if month == 6:
            member = ctx.message.author
            if member.nick and member.nick[-1] == "🌈":
                await self.bot.say("Your nickname already ends in a rainbow!")
            elif member.name[-1] == "🌈" and not member.nick:
                await self.bot.say("Your name already ends in a rainbow!")
            else:
                await self.bot.change_nickname(member, member.display_name + " 🌈")
                await self.bot.say("Your nickname is now \"{} \"!".format(member.display_name))  
        else:
            await self.bot.say("This month is not colorful enough!")
            
    @commands.command(pass_context=True)
    async def norainbow(self, ctx):
        """Tired of it."""
        if not await self.verify_botcmds(ctx): return
        member = ctx.message.author
        if member.nick and member.nick[-1] == "🌈":
            await self.bot.say("Your nickname is now \"{}\"!".format(member.display_name[0:-1].strip()))
            await self.bot.change_nickname(member, member.display_name[0:-1])
        elif member.name[-1] == "🌈":
            await self.bot.say("Your username is the one with the rainbow!")
        else:
            await self.bot.say("You don't have a rainbow!")

    @commands.command(pass_context=True)
    async def spooky(self, ctx):
        """Spookybrew"""
        if not await self.verify_botcmds(ctx): return
        month = datetime.date.today().month
        if month == 10:
            member = ctx.message.author
            if member.nick and member.nick[-1] == "🎃":
                await self.bot.say("Your nickname already ends in a pumpkin!")
            elif member.name[-1] == "🎃" and not member.nick:
                await self.bot.say("Your name already ends in a pumpkin!")
            else:
                await self.bot.change_nickname(member, member.display_name + " 🎃")
                await self.bot.say("Your nickname is now \"{} \"!".format(member.display_name))  
        else:
            await self.bot.say("This month is not spooky enough!")

    @commands.command(pass_context=True)
    async def nospooky(self, ctx):
        """Tired of it."""
        if not await self.verify_botcmds(ctx): return
        member = ctx.message.author
        if member.nick and member.nick[-1] == "🎃":
            await self.bot.say("Your nickname is now \"{}\"!".format(member.display_name[0:-1].strip()))
            await self.bot.change_nickname(member, member.display_name[0:-1])
        elif member.name[-1] == "🎃":
            await self.bot.say("Your username is the one with the pumpkin!")
        else:
            await self.bot.say("You don't have a pumpkin!")
            
    @commands.command(pass_context=True)
    async def turkey(self, ctx):
        """Turkeybrew"""
        if not await self.verify_botcmds(ctx): return
        month = datetime.date.today().month
        if month == 11:
            member = ctx.message.author
            if member.nick and member.nick[-1] == "🦃":
                await self.bot.say("Your nickname already ends in a turkey!")
            elif member.name[-1] == "🦃" and not member.nick:
                await self.bot.say("Your name already ends in a turkey!")
            else:
                await self.bot.change_nickname(member, member.display_name + " 🦃")
                await self.bot.say("Your nickname is now \"{} \"!".format(member.display_name))  
        else:
            await self.bot.say("This month is not thankful enough!")

    @commands.command(pass_context=True)
    async def noturkey(self, ctx):
        """Tired of it."""
        if not await self.verify_botcmds(ctx): return
        member = ctx.message.author
        if member.nick and member.nick[-1] == "🦃":
            await self.bot.say("Your nickname is now \"{}\"!".format(member.display_name[0:-1].strip()))
            await self.bot.change_nickname(member, member.display_name[0:-1])
        elif member.name[-1] == "🦃":
            await self.bot.say("Your username is the one with the turkey!")
        else:
            await self.bot.say("You don't have a turkey!")
            
    @commands.command(pass_context=True)
    async def xmasthing(self, ctx):
        """It's xmas time."""
        if not await self.verify_botcmds(ctx): return
        month = datetime.date.today().month
        if month == 12:
            member = ctx.message.author
            if member.nick and member.nick[-1] == "🎄":
                await self.bot.say("Your nickname already ends in an xmas tree!")
            elif member.name[-1] == "🎄" and not member.nick:
                await self.bot.say("Your name already ends in an xmas tree!")
            else:
                await self.bot.change_nickname(member, member.display_name + " 🎄")
                await self.bot.say("Your nickname is now \"{} \"!".format(member.display_name))  
        else:
            await self.bot.say("This month is not christmassy enough!")
            
    @commands.command(pass_context=True)
    async def noxmasthing(self, ctx):
        """Tired of it."""
        if not await self.verify_botcmds(ctx): return
        member = ctx.message.author
        if member.nick and member.nick[-1] == "🎄":
            await self.bot.say("Your nickname is now \"{}\"!".format(member.display_name[0:-1].strip()))
            await self.bot.change_nickname(member, member.display_name[0:-1])
        elif member.name[-1] == "🎄":
            await self.bot.say("Your username is the one with the xmas tree!")
        else:
            await self.bot.say("You don't have an xmas tree!")

def setup(bot):
    bot.add_cog(Extras(bot))
