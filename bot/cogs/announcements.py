import discord
from discord.ext import commands, tasks
import datetime

class Announcements(commands.Cog):
    """Announcements"""


    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⏰'

        # self.bigben.start()

    @tasks.loop(hours=1.0)
    async def bigben(self):
        for guild in self.guilds:
            channels = guild.voice_channels
            max_user_channel = max(channels, lambda c: len(c.members))
            await max_user_channel.connect()
        print('DONG')



def setup(bot):
    bot.add_cog(Announcements(bot))